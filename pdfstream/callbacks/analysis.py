import typing as tp
from configparser import ConfigParser, Error
from pathlib import Path

import event_model
import matplotlib.pyplot as plt
import numpy as np
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.callbacks.broker import LiveImage
from bluesky.callbacks.stream import LiveDispatcher
from databroker.v2 import Broker
from event_model import RunRouter
from matplotlib.gridspec import GridSpec
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from suitcase.csv import Serializer as CSVSerializer
from suitcase.json_metadata import Serializer as JsonSerializer
from suitcase.tiff_series import Serializer as TiffSerializer

import pdfstream.callbacks.from_descriptor as from_desc
import pdfstream.callbacks.from_event as from_event
import pdfstream.callbacks.from_start as from_start
import pdfstream.integration.tools as integ
from pdfstream.callbacks.basic import LiveMaskedImage, LiveWaterfall, NumpyExporter, SmartScalarPlot
from pdfstream.units import LABELS
from pdfstream.vend.formatters import SpecialStr

try:
    from diffpy.pdfgetx import PDFConfig, PDFGetter
except ImportError:
    pass


class BasicAnalysisConfig(ConfigParser):
    """The basic configuration that is shared by analysis and calibration."""

    @property
    def raw_db(self):
        name = self.get("DATABASE", "raw_db", fallback=None)
        if name:
            from databroker import catalog
            return catalog[name]
        return None

    @property
    def dark_identifier(self):
        return self.get("METADATA", "dk_identifier")

    @property
    def dk_id_key(self):
        return self.get("METADATA", "dk_id_key")

    @property
    def composition_key(self):
        return self.get("METADATA", "composition_key")

    @property
    def wavelength_key(self):
        return self.get("METADATA", "wavelength_key")


class AnalysisConfig(BasicAnalysisConfig):
    """The configuration for analysis callbacks."""

    @property
    def calibration_md_key(self):
        return self.get("METADATA", "calibration_md_key")

    @property
    def mask_setting(self):
        section = self["MASK SETTING"]
        return {
            "alpha": section.getfloat("alpha"),
            "edge": section.getint("edge"),
            "lower_thresh": section.getfloat("lower_thresh"),
            "upper_thresh": section.getfloat("upper_thresh")
        }

    @property
    def integ_setting(self):
        section = self["INTEGRATION SETTING"]
        return {
            "npt": section.getint("npt"),
            "correctSolidAngle": section.getboolean("correctSolidAngle"),
            "polarization_factor": section.getfloat("polarization_factor"),
            "method": section.get("method"),
            "normalization_factor": section.getfloat("normalization_factor"),
            "unit": "q_A^-1"
        }

    @property
    def trans_setting(self):
        section = self["TRANSFORMATION SETTING"]
        return {
            "rpoly": section.getfloat("rpoly"),
            "qmaxinst": section.getfloat("qmaxinst"),
            "qmin": section.getfloat("qmin"),
            "qmax": section.getfloat("qmax")
        }

    @property
    def grid_config(self):
        section = self["PDF SETTING"]
        return {
            "rmin": section.getfloat("rmin"),
            "rmax": section.getfloat("rmax"),
            "rstep": section.getfloat("rstep")
        }

    def to_dict(self):
        """Convert the configuration to a dictionary."""
        return {s: dict(self.items(s)) for s in self.sections()}


class AnalysisStream(LiveDispatcher):
    """The secondary stream for data analysis.

    It inject the configuration into start document and emit processed data to the subscribers.
    """

    def __init__(self, config: AnalysisConfig, *, raw_db: Broker = None):
        super().__init__()
        self.config = config
        self.cache = {}
        self.db = config.raw_db if raw_db is None else raw_db

    def start(self, doc, _md=None):
        self.cache = dict()
        self.cache["start"] = doc
        self.cache["ai"] = from_start.query_ai(
            doc,
            calibration_md_key=self.config.calibration_md_key
        )
        self.cache["bt_info"] = from_start.query_bt_info(
            doc,
            composition_key=self.config.composition_key,
            wavelength_key=self.config.wavelength_key,
            default_composition="Ni"
        )
        self.cache["indeps"] = from_start.get_indeps(doc, exclude={"time"})
        super().start(dict(**doc, an_config=self.config.to_dict()))

    def event_page(self, doc):
        for event_doc in event_model.unpack_event_page(doc):
            self.event(event_doc)

    def descriptor(self, doc):
        self.cache["det_name"] = from_desc.find_one_image(doc)
        self.cache["dk_img"] = from_start.query_dk_img(
            self.cache["start"],
            db=self.db,
            dk_id_key=self.config.dk_id_key,
            det_name=self.cache["det_name"]
        )
        super().descriptor(doc)

    def event(self, doc, _md=None):
        raw_img = from_event.get_image_from_event(doc, det_name=self.cache["det_name"])
        indep_data = {key: doc["data"][key] for key in self.cache["indeps"]}
        an_data = process(
            raw_img=raw_img,
            dk_img=self.cache["dk_img"],
            ai=self.cache["ai"],
            integ_setting=self.config.integ_setting,
            mask_setting=self.config.mask_setting,
            pdfgetx_setting=dict(
                self.cache["bt_info"],
                **self.config.trans_setting,
                **self.config.grid_config
            )
        )
        data = dict(**indep_data, **an_data)
        self.process_event(EventDoc(data=data, descriptor=doc["descriptor"]))

    def stop(self, doc, _md=None):
        self.cache = {}
        super().stop(doc)


def process(
    *,
    raw_img: np.ndarray,
    dk_img: np.ndarray = None,
    ai: AzimuthalIntegrator = None,
    integ_setting: dict = None,
    mask_setting: dict = None,
    pdfgetx_setting: dict = None,
) -> dict:
    """The function to process the data from event."""
    data = dict()
    # dark subtraction
    if dk_img is None:
        dk_img = np.zeros_like(raw_img)
    else:
        data.update({"dk_image": dk_img})
    final_image = np.subtract(raw_img, dk_img)
    data.update({"dk_sub_image": final_image})
    # return the data if no calibration metadata
    if ai is None:
        return data
    # auto masking
    final_mask, _ = integ.auto_mask(final_image, ai, mask_setting=mask_setting)
    data.update({"mask": final_mask})
    # integration
    x, y = ai.integrate1d(final_image, mask=final_mask, **integ_setting)
    chi_max_ind = np.argmax(y)
    data.update({"chi_Q": x, "chi_I": y, "chi_max": y[chi_max_ind], "chi_argmax": x[chi_max_ind]})
    # transformation
    pdfconfig = PDFConfig(dataformat="QA", **pdfgetx_setting)
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


class EventDoc(dict):
    """A simplified event document for callbacks.

    It only contains two necessary key: data and descriptor. The data is the dictionary of data key and data
    value and the descriptor is the uid of the descriptor from the original event.
    """

    def __init__(self, data: dict, descriptor: str, **kwargs):
        super().__init__(data=data, descriptor=descriptor, **kwargs)

    @property
    def data(self):
        return self["data"]

    @data.setter
    def data(self, val: dict):
        self["data"] = val

    @property
    def descriptor(self):
        return self["descriptor"]

    @descriptor.setter
    def descriptor(self, val: dict):
        self["descriptor"] = val


class BasicExportConfig(ConfigParser):
    """Basic configuration that is shared by export and calibration."""

    @property
    def tiff_base(self):
        section = self["FILE SYSTEM"]
        dir_path = section.get("tiff_base")
        if not dir_path:
            raise Error("Missing tiff_base in configuration.")
        path = Path(dir_path)
        return path

    @tiff_base.setter
    def tiff_base(self, value: str):
        self.set("FILE SYSTEM", "tiff_base", value)


class ExportConfig(BasicExportConfig):
    """The configuration of exporter."""
    @property
    def tiff_setting(self):
        section = self["TIFF SETTING"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"file_prefix": SpecialStr(section.get("file_prefix"))}

    @property
    def json_setting(self):
        section = self["JSON SETTING"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"file_prefix": SpecialStr(section.get("file_prefix"))}

    @property
    def csv_setting(self):
        section = self["CSV SETTING"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"file_prefix": SpecialStr(section.get("file_prefix"))}

    @property
    def npy_setting(self):
        section = self["NPY SETTING"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"file_prefix": SpecialStr(section.get("file_prefix"))}


class Exporter(RunRouter):
    """Export the processed data to file systems, including."""

    def __init__(self, config: ExportConfig):
        factory = ExporterFactory(config)
        super().__init__([factory])


class ExporterFactory:
    """The factory for the exporter run router."""

    def __init__(self, config: ExportConfig):
        self.config = config
        tiff_base = self.config.tiff_base
        tiff_base.mkdir(exist_ok=True, parents=True)
        self.callbacks = []
        if self.config.tiff_setting is not None:
            cb = TiffSerializer(
                str(tiff_base.joinpath("images")),
                **self.config.tiff_setting
            )
            self.callbacks.append(cb)
        if self.config.json_setting is not None:
            cb = JsonSerializer(
                str(tiff_base.joinpath("metadata")),
                **self.config.json_setting
            )
            self.callbacks.append(cb)
        if self.config.csv_setting is not None:
            cb = CSVSerializer(
                str(tiff_base.joinpath("datasheets")),
                **self.config.csv_setting
            )
            self.callbacks.append(cb)
        if self.config.csv_setting is not None:
            cb = NumpyExporter(
                str(tiff_base.joinpath("arrays")),
                **self.config.npy_setting
            )
            self.callbacks.append(cb)

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name != "start":
            return [], []
        return self.callbacks, []


class VisConfig(ConfigParser):
    """The configuration of visualization."""

    @property
    def vis_best_effort(self):
        section = self["VIS BEST EFFORT"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {}

    @property
    def vis_masked_image(self):
        section = self["VIS MASKED IMAGE"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "cmap": section.get("cmap")
        }

    @property
    def vis_dk_sub_image(self):
        section = self["VIS DK SUB IMAGE"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"cmap": section.get("cmap", fallback="viridis")}

    @property
    def vis_chi(self):
        section = self["VIS CHI"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.chi[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.chi[1])
        }

    @property
    def vis_iq(self):
        section = self["VIS IQ"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.iq[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.iq[1])
        }

    @property
    def vis_sq(self):
        section = self["VIS SQ"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.sq[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.sq[1])
        }

    @property
    def vis_fq(self):
        section = self["VIS FQ"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.fq[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.fq[1])
        }

    @property
    def vis_gr(self):
        section = self["VIS GR"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.gr[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.gr[1])
        }

    @property
    def vis_gr_max(self):
        section = self["VIS GR MAX"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"ylabel": section.get("ylabel", fallback=LABELS.gr[1])}

    @property
    def vis_gr_argmax(self):
        section = self["VIS GR ARGMAX"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"ylabel": section.get("ylabel", fallback=LABELS.gr[0])}

    @property
    def vis_chi_max(self):
        section = self["VIS CHI MAX"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"ylabel": section.get("ylabel", fallback=LABELS.chi[1])}

    @property
    def vis_chi_argmax(self):
        section = self["VIS CHI ARGMAX"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"ylabel": section.get("ylabel", fallback=LABELS.chi[0])}


class Visualizer(RunRouter):
    """Visualize the analyzed data. It can be subscribed to a live dispatcher."""

    def __init__(self, config: VisConfig):
        self._factory = VisFactory(config)
        super(Visualizer, self).__init__([self._factory])

    def show_figs(self):
        """Show all the figures in the callbacks in the factory."""
        for cb in self._factory.cb_lst:
            if isinstance(cb, (LiveImage, LiveMaskedImage)):
                cb.cs._fig.show()
            elif isinstance(cb, LiveWaterfall):
                cb.waterfall.fig.show()
            elif isinstance(cb, SmartScalarPlot):
                cb.ax.figure.show()
        return


class VisFactory:
    """The factory of visualization callbacks."""

    def __init__(self, config: VisConfig):
        self.config = config
        self.cb_lst = []
        if self.config.vis_best_effort is not None:
            cb = BestEffortCallback()
            cb.disable_table()
            cb.disable_baseline()
            cb.disable_heading()
            self.cb_lst.append(cb)
        if self.config.vis_dk_sub_image is not None:
            self.cb_lst.append(
                LiveImage("dk_sub_image", **self.config.vis_dk_sub_image)
            )
        if self.config.vis_masked_image is not None:
            self.cb_lst.append(
                LiveMaskedImage("dk_sub_image", "mask", **self.config.vis_masked_image)
            )
        for xfield, yfield, vis_config in [
            ("chi_Q", "chi_I", self.config.vis_chi),
            ("iq_Q", "iq_I", self.config.vis_iq),
            ("sq_Q", "sq_S", self.config.vis_sq),
            ("fq_Q", "fq_F", self.config.vis_fq),
            ("gr_r", "gr_G", self.config.vis_gr)
        ]:
            if vis_config is not None:
                self.cb_lst.append(
                    LiveWaterfall(xfield, yfield, **vis_config)
                )
        fig = plt.figure()
        axes = (fig.add_subplot(grid) for grid in GridSpec(2, 2))
        for field, vis_config in [
            ("chi_max", self.config.vis_chi_max),
            ("chi_argmax", self.config.vis_chi_argmax),
            ("gr_max", self.config.vis_gr_max),
            ("gr_argmax", self.config.vis_gr_argmax)
        ]:
            if vis_config is not None:
                self.cb_lst.append(
                    SmartScalarPlot(field, ax=next(axes), **vis_config)
                )

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name != "start":
            return [], []
        return self.cb_lst, []
