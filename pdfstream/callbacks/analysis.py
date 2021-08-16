import copy
import datetime
import typing as tp
from configparser import ConfigParser
from pathlib import Path

import event_model
import matplotlib.pyplot as plt
import numpy as np
from bluesky.callbacks.stream import LiveDispatcher
from databroker.v1 import Broker
from event_model import RunRouter
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from suitcase.csv import Serializer as CSVSerializer
from suitcase.json_metadata import Serializer as JsonSerializer

import pdfstream
import pdfstream.callbacks.from_descriptor as from_desc
import pdfstream.callbacks.from_event as from_event
import pdfstream.callbacks.from_start as from_start
import pdfstream.integration.tools as integ
import pdfstream.io as io
from pdfstream.callbacks.basic import MyLiveImage, LiveMaskedImage, LiveWaterfall, StackedNumpyTextExporter, \
    SmartScalarPlot, MyTiffSerializer, CalibrationExporter, NumpyExporter
from pdfstream.errors import ValueNotFoundError
from pdfstream.units import LABELS
from pdfstream.vend.formatters import SpecialStr

try:
    from diffpy.pdfgetx import PDFConfig, PDFGetter

    _PDFGETX_AVAILABLE = True
except ImportError:
    _PDFGETX_AVAILABLE = False


class BasicAnalysisConfig(ConfigParser):
    """The basic configuration that is shared by analysis and calibration."""

    @property
    def raw_db(self) -> str:
        return self.get("DATABASE", "raw_db", fallback="")

    @property
    def dark_identifier(self):
        return self.get("METADATA", "dk_identifier", fallback="dark_frame")

    @property
    def dk_id_key(self):
        return self.get("METADATA", "dk_id_key", fallback="sc_dk_field_uid")

    @property
    def composition_key(self):
        return self.get("METADATA", "composition_key", fallback="sample_composition")

    @property
    def wavelength_key(self):
        return self.get("METADATA", "wavelength_key", fallback="bt_wavelength")

    def to_dict(self):
        """Convert the configuration to a dictionary."""
        return {s: dict(self.items(s)) for s in self.sections()}

    def read_user_config(self, user_config):
        self.read_dict({"ANALYSIS": user_config})


class AnalysisConfig(BasicAnalysisConfig):
    """The configuration for analysis callbacks."""

    def __init__(self, *args, **kwargs):
        super(AnalysisConfig, self).__init__(*args, **kwargs)
        self.add_section("DATABASE")
        self.add_section("METADATA")
        self.add_section("ANALYSIS")

    @property
    def calibration_md_key(self):
        return self.get("METADATA", "calibration_md_key", fallback="calibration_md")

    @property
    def sample_name_key(self):
        return self.get("METADATA", "sample_name_key", fallback="sample_name")

    @property
    def auto_mask(self):
        return self.getboolean("ANALYSIS", "auto_mask", fallback=True)

    @property
    def user_mask(self):
        mask_file = self.get("ANALYSIS", "user_mask", fallback="")
        if not mask_file:
            return None
        return io.load_matrix_flexible(mask_file)

    @property
    def mask_setting(self):
        return {
            "alpha": self.getfloat("ANALYSIS", "alpha", fallback=2.5),
            "edge": self.getint("ANALYSIS", "edge", fallback=20),
            "lower_thresh": self.getfloat("ANALYSIS", "lower_thresh", fallback=0.),
            "upper_thresh": self.getfloat("ANALYSIS", "upper_thresh", fallback=None)
        }

    @property
    def integ_setting(self):
        return {
            "npt": self.getint("ANALYSIS", "npt", fallback=2048),
            "correctSolidAngle": self.getboolean("ANALYSIS", "correctSolidAngle", fallback=False),
            "polarization_factor": self.getfloat("ANALYSIS", "polarization_factor", fallback=0.99),
            "method": self.get("ANALYSIS", "method", fallback="bbox,csr,cython"),
            "normalization_factor": self.getfloat("ANALYSIS", "normalization_factor", fallback=1.),
            "unit": "2th_deg"
        }

    @property
    def trans_setting(self):
        return {
            "rpoly": self.getfloat("ANALYSIS", "rpoly", fallback=1.2),
            "qmaxinst": self.getfloat("ANALYSIS", "qmaxinst", fallback=24.),
            "qmin": self.getfloat("ANALYSIS", "qmin", fallback=0.),
            "qmax": self.getfloat("ANALYSIS", "qmax", fallback=22.),
            "rmin": self.getfloat("ANALYSIS", "rmin", fallback=0.),
            "rmax": self.getfloat("ANALYSIS", "rmax", fallback=30.),
            "rstep": self.getfloat("ANALYSIS", "rstep", fallback=0.01),
            "dataformat": "QA"
        }


class AnalysisStream(LiveDispatcher):
    """The secondary stream for data analysis.

    It inject the configuration into start document and emit processed data to the subscribers.
    """

    def __init__(self, config: AnalysisConfig):
        super(AnalysisStream, self).__init__()
        self.init_config = config
        self.config = None
        db_name = config.raw_db
        self.db = Broker.named(db_name) if db_name else None
        self.start_doc = {}
        self.ai = None
        self.bt_info = {}
        self.image_key = ""
        self.dark_image = None

    def start(self, doc, _md=None):
        io.server_message("Receive the start of '{}'.".format(doc["uid"]))
        self.clear_cache()
        # copy the default config and read the user config
        self.config = copy.deepcopy(self.init_config)
        self.config.read_user_config(doc.get("user_config", {}))
        # record start doc for later use
        self.start_doc = doc
        # find ai
        try:
            self.ai = from_start.query_ai(
                doc,
                calibration_md_key=self.config.calibration_md_key
            )
            io.server_message("Read the calibration data in the start.")
        except ValueNotFoundError as error:
            self.ai = None
            io.server_message("Failed to find calibration data: {}.".format(str(error)))
        # find bt info
        try:
            self.bt_info = from_start.query_bt_info(
                doc,
                composition_key=self.config.composition_key,
                wavelength_key=self.config.wavelength_key,
                default_composition="Ni"
            )
        except ValueNotFoundError as error:
            self.bt_info = {}
            io.server_message("Encounter error when searching the metadata: {}.".format(str(error)))
        # create new start
        new_start = dict(**doc, an_config=self.config.to_dict(), pdfstream_version=pdfstream.__version__)
        return super(AnalysisStream, self).start(new_start)

    def event_page(self, doc):
        for event_doc in event_model.unpack_event_page(doc):
            self.event(event_doc)

    def descriptor(self, doc):
        self.image_key = from_desc.find_one_image(doc)
        io.server_message("Find the data key '{}' in the stream '{}'.".format(self.image_key, doc["name"]))
        try:
            self.dark_image = from_start.query_dk_img(
                self.start_doc,
                db=self.db,
                dk_id_key=self.config.dk_id_key,
                det_name=self.image_key
            )
        except ValueNotFoundError as error:
            self.dark_image = None
            io.server_message("Failed to find the dark: " + str(error))
        return super(AnalysisStream, self).descriptor(doc)

    def event(self, doc, _md=None):
        io.server_message("Start processing the event {}.".format(doc["seq_num"]))
        data = self.process_data(doc)
        io.server_message("Finish processing the event {}.".format(doc["seq_num"]))
        return self.process_event(dict(data=data, descriptor=doc["descriptor"]))

    def stop(self, doc, _md=None):
        io.server_message("Receive the stop of '{}'.".format(doc["run_start"]))
        return super(AnalysisStream, self).stop(doc)

    def process_data(self, doc) -> dict:
        """Process the data in the event doc. Return a dictionary of processed data."""
        # the raw image in the data
        raw_img = from_event.get_image_from_event(doc, det_name=self.image_key)
        # copy the data
        raw_data = {k: copy.copy(v) for k, v in doc["data"].items() if k != self.image_key}
        # process the data output a dictionary
        an_data = process(
            raw_img=raw_img,
            ai=self.ai,
            user_mask=self.config.user_mask,
            auto_mask=self.config.auto_mask,
            dk_img=self.dark_image,
            integ_setting=self.config.integ_setting,
            mask_setting=self.config.mask_setting,
            pdfgetx_setting=dict(
                **self.bt_info,
                **self.config.trans_setting
            )
        )
        # the final output data is a combination of the independent variables and processed data
        return dict(**raw_data, **an_data)

    def clear_cache(self):
        """Clear the cache."""
        self.config = None
        self.start_doc = {}
        self.ai = None
        self.bt_info = {}
        self.image_key = ""
        self.dark_image = None


def process(
    *,
    raw_img: np.ndarray,
    ai: tp.Union[None, AzimuthalIntegrator],
    user_mask: np.ndarray = None,
    auto_mask: bool = True,
    dk_img: np.ndarray = None,
    integ_setting: dict = None,
    mask_setting: dict = None,
    pdfgetx_setting: dict = None,
) -> dict:
    """The function to process the data from event."""
    # initialize the data dictionary
    data = {
        "dk_sub_image": raw_img,
        "mask": np.zeros_like(raw_img),
        "chi_2theta": np.array([0.]),
        "chi_Q": np.array([0.]),
        "chi_I": np.array([0.]),
        "chi_max": np.float(0.),
        "chi_argmax": np.float(0.),
        "iq_Q": np.array([0.]),
        "iq_I": np.array([0.]),
        "sq_Q": np.array([0.]),
        "sq_S": np.array([0.]),
        "fq_Q": np.array([0.]),
        "fq_F": np.array([0.]),
        "gr_r": np.array([0.]),
        "gr_G": np.array([0.]),
        "gr_max": np.float(0.),
        "gr_argmax": np.float(0.)
    }
    # dark subtraction
    if dk_img is not None:
        data["dk_sub_image"] = np.subtract(raw_img, dk_img)
    # if no calibration, output data now
    if ai is None:
        return data
    # do auto masking if specified
    if auto_mask:
        data["mask"], _ = integ.auto_mask(data["dk_sub_image"], ai, mask_setting=mask_setting, user_mask=user_mask)
    elif user_mask is not None:
        data["mask"] = user_mask
    # integration
    tth, y = ai.integrate1d(data["dk_sub_image"], mask=data["mask"], **integ_setting)
    x = 4. * np.pi / (ai.get_wavelength() * 1e10) * np.sin(np.deg2rad(tth / 2.))
    chi_max_ind = np.argmax(y)
    data.update(
        {
            "chi_2theta": tth, "chi_Q": x, "chi_I": y, "chi_max": x[chi_max_ind], "chi_argmax": y[chi_max_ind]
        }
    )
    # transformation
    if not _PDFGETX_AVAILABLE:
        io.server_message("diffpy.pdfgetx is not installed. No use [0.] for all the relevant data.")
        return data
    pdfconfig = PDFConfig(**pdfgetx_setting)
    pdfgetter = PDFGetter(pdfconfig)
    pdfgetter(x, y)
    iq, sq, fq, gr = pdfgetter.iq, pdfgetter.sq, pdfgetter.fq, pdfgetter.gr
    gr_max_ind = np.argmax(gr[1])
    data.update(
        {
            "iq_Q": iq[0], "iq_I": iq[1], "sq_Q": sq[0], "sq_S": sq[1], "fq_Q": fq[0], "fq_F": fq[1],
            "gr_r": gr[0], "gr_G": gr[1], "gr_max": gr[1][gr_max_ind], "gr_argmax": gr[0][gr_max_ind]
        }
    )
    return data


class ExportConfig(ConfigParser):
    """The configuration of exporter."""

    def __init__(self, *args, **kwargs):
        super(ExportConfig, self).__init__(*args, **kwargs)
        self.add_section("SUITCASE")

    @property
    def calib_identifier(self):
        return self.get("METADATA", "calib_identifier", fallback="is_calibration")

    def get_exports(self):
        return set(
            self.get("SUITCASE", "exports", fallback="poni,tiff,mask,json,csv,txt").replace(" ", "").split(","))

    def get_file_prefix(self):
        return SpecialStr(
            self.get("SUITCASE", "file_prefix", fallback="{start[original_run_uid]}_{start[readable_time]}_"))

    @property
    def directory_template(self):
        return SpecialStr(self.get("SUITCASE", "directory_template", fallback="{start[sample_name]}_data"))

    @property
    def tiff_base(self):
        """Settings for the base folder."""
        dir_path = self.get("SUITCASE", "tiff_base")
        if not dir_path:
            dir_path = "~/pdfstream_data"
            io.server_message("Missing tiff_base in configuration. Use '{}'".format(dir_path))
        path = Path(dir_path).expanduser()
        return path

    @tiff_base.setter
    def tiff_base(self, value: str):
        self.set("SUITCASE", "tiff_base", value)

    @property
    def tiff_setting(self):
        return {
            "astype": self.get("SUITCASE", "tiff_astype", fallback="float32"),
            "bigtiff": self.getboolean("SUITCASE", "tiff_bigtiff", fallback=False),
            "byteorder": self.get("SUITCASE", "tiff_byteorder", fallback=None),
            "imagej": self.get("SUITCASE", "tiff_imagej", fallback=False)
        }


class Exporter(RunRouter):
    """Export the processed data to file systems. Add readable_time to start doc."""

    def __init__(self, config: ExportConfig):
        factory = ExporterFactory(config)
        super().__init__([factory])
        io.server_message("Data will be exported in '{}'.".format(str(config.tiff_base)))

    def start(self, start_doc):
        io.server_message("Inject 'readable_time' in the start of '{}'.".format(start_doc["uid"]))
        start_doc = copy.deepcopy(start_doc)
        start_doc["readable_time"] = datetime.datetime.fromtimestamp(start_doc["time"]).strftime(
            "%Y%m%d-%H%M%S")
        return super(Exporter, self).start(start_doc)

    def event(self, doc):
        io.server_message("Export data in the event {}.".format(doc["seq_num"]))
        return super(Exporter, self).event(doc)

    def stop(self, doc):
        io.server_message("Finish exporting data for '{}'.".format(doc["run_start"]))
        return super(Exporter, self).stop(doc)


class ExporterFactory:
    """The factory for the exporter run router."""

    def __init__(self, config: ExportConfig):
        self.config = config

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name != "start":
            return [], []
        data_folder = self.config.tiff_base.joinpath(self.config.directory_template.format(start=doc))
        data_folder.mkdir(exist_ok=True, parents=True)
        callbacks = []
        exports = self.config.get_exports()
        file_prefix = self.config.get_file_prefix()
        if "tiff" in exports:
            cb = MyTiffSerializer(
                str(data_folder.joinpath("dark_sub")),
                file_prefix=file_prefix,
                data_keys=["dk_sub_image"],
                **self.config.tiff_setting
            )
            callbacks.append(cb)
        if "mask" in exports:
            cb = NumpyExporter(
                str(data_folder.joinpath("mask")),
                file_prefix=file_prefix,
                data_keys=["mask"]
            )
            callbacks.append(cb)
        if "json" in exports:
            cb = JsonSerializer(
                str(data_folder.joinpath("meta")),
                file_prefix=file_prefix
            )
            callbacks.append(cb)
        if "csv" in exports:
            cb = CSVSerializer(
                str(data_folder.joinpath("scalar_data")),
                file_prefix=file_prefix
            )
            callbacks.append(cb)
        if "txt" in exports:
            cb = StackedNumpyTextExporter(
                file_prefix,
                str(data_folder.joinpath("integration")), ("chi_2theta", "chi_I"), "_mean_tth.chi",
                str(data_folder.joinpath("integration")), ("chi_Q", "chi_I"), "_mean_q.chi",
                str(data_folder.joinpath("sq")), ("sq_Q", "sq_S"), ".sq",
                str(data_folder.joinpath("fq")), ("fq_Q", "fq_F"), ".fq",
                str(data_folder.joinpath("gr")), ("gr_r", "gr_G"), ".gr",
            )
            callbacks.append(cb)
        if "poni" in exports and doc.get(self.config.calib_identifier, False):
            cb = CalibrationExporter(str(data_folder.joinpath("calib")), file_prefix=file_prefix)
            callbacks.append(cb)
        return callbacks, []


def _get_vlim(image: np.ndarray) -> tp.Tuple[float, float]:
    """Get the vmin and vmax from a image."""
    m = np.mean(image)
    std = np.std(image)
    return max(m - 2 * std, 0), m + 2 * std


class VisConfig(ConfigParser):
    """The configuration of visualization."""

    def __init__(self, *args, **kwargs):
        super(VisConfig, self).__init__(*args, **kwargs)
        self.add_section("VISUALIZATION")

    def get_visualizers(self):
        return set(
            self.get(
                "VISUALIZATION",
                "visualizers",
                fallback="dk_sub_image,masked_image,chi,chi_2theta,iq,sq,fq,gr,chi_max,chi_argmax,gr_max,gr_argmax"
            ).replace(" ", "").split(",")
        )

    @property
    def vis_masked_image(self):
        return {
            "cmap": "viridis",
            "limit_func": _get_vlim
        }

    @property
    def vis_dk_sub_image(self):
        return {
            "cmap": "viridis",
            "limit_func": _get_vlim
        }

    @property
    def vis_2theta(self):
        return {
            "xlabel": LABELS.tth[0],
            "ylabel": LABELS.tth[1]
        }

    @property
    def vis_chi(self):
        return {
            "xlabel": LABELS.chi[0],
            "ylabel": LABELS.chi[1]
        }

    @property
    def vis_iq(self):
        return {
            "xlabel": LABELS.iq[0],
            "ylabel": LABELS.iq[1]
        }

    @property
    def vis_sq(self):
        return {
            "xlabel": LABELS.sq[0],
            "ylabel": LABELS.sq[1]
        }

    @property
    def vis_fq(self):
        return {
            "xlabel": LABELS.fq[0],
            "ylabel": LABELS.fq[1]
        }

    @property
    def vis_gr(self):
        return {
            "xlabel": LABELS.gr[0],
            "ylabel": LABELS.gr[1]
        }


class Visualizer(RunRouter):
    """Visualize the analyzed data. It can be subscribed to a live dispatcher."""

    def __init__(self, config: VisConfig):
        self._factory = VisFactory(config)
        super(Visualizer, self).__init__([self._factory])

    def show_figs(self):
        """Show all the figures in the callbacks in the factory."""
        return self._factory.show()


class VisFactory:
    """The factory of visualization callbacks."""

    def __init__(self, config: VisConfig):
        self.config = config
        self.cb_lst = []
        visualizers = self.config.get_visualizers()
        # images
        if "dk_sub_image" in visualizers:
            self.cb_lst.append(
                MyLiveImage("dk_sub_image", **self.config.vis_dk_sub_image)
            )
        if "masked_image" in visualizers:
            self.cb_lst.append(
                LiveMaskedImage("dk_sub_image", "mask", **self.config.vis_masked_image)
            )
        # one dimensional array waterfall
        for xfield, yfield, tag, vis_config in [
            ("chi_2theta", "chi_I", "chi", self.config.vis_2theta),
            ("chi_Q", "chi_I", "chi", self.config.vis_chi),
            ("iq_Q", "iq_I", "iq", self.config.vis_iq),
            ("sq_Q", "sq_S", "sq", self.config.vis_sq),
            ("fq_Q", "fq_F", "fq", self.config.vis_fq),
            ("gr_r", "gr_G", "gr", self.config.vis_gr)
        ]:
            if tag in visualizers:
                fig = plt.figure()
                self.cb_lst.append(
                    LiveWaterfall(xfield, yfield, ax=fig.add_subplot(111), **vis_config)
                )
                fig.show()
        for field in ("gr_max", "gr_argmax", "chi_max", "chi_argmax"):
            if field in visualizers:
                fig = plt.figure()
                ax = fig.add_subplot(111)
                self.cb_lst.append(
                    SmartScalarPlot(field, ax=ax, marker="o")
                )
                fig.show()

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name != "start":
            return [], []
        return self.cb_lst, []

    def show(self):
        for cb in self.cb_lst:
            try:
                cb.show()
            except AttributeError:
                pass
        return
