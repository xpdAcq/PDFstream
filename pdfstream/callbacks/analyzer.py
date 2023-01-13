import copy
import subprocess
import typing as T
from functools import lru_cache
from pathlib import Path
from tempfile import TemporaryDirectory

import event_model
import numpy as np
from frozendict import frozendict
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from pyFAI.io import DefaultAiWriter
from pyFAI.io.ponifile import PoniFile
from tifffile import TiffWriter

import pdfstream.io as io
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.datakeys import DataKeys
from pdfstream.vend.masking import generate_binner, mask_img_pyfai
from pdfstream.data import ni_dspacing_file

try:
    from diffpy.pdfgetx import PDFConfig, PDFGetter

    _PDFGETX_AVAILABLE = True
except ImportError:
    _PDFGETX_AVAILABLE = False

Keys = T.List[str]
Data = T.Dict[str, T.Any]
Units = T.List[str]
DeviceName = str
CalibData = frozendict
CalibKeys = T.List[str]


def _add_kwargs(lst: list, dct: dict) -> list:
    for k, v in dct.items():
        lst.append("--{}".format(k))
        lst.append(str(v))
    return lst


def _load_calib(poni_file: str) -> CalibData:
    pf = PoniFile()
    pf.read_from_file(poni_file)
    dct = pf.as_dict()
    if "detector_config" in dct:
        del dct["detector_config"]
    if "poni_version" in dct:
        del dct["poni_version"]
    return frozendict(dict(dct))


def _parse_to_cailb(data: Data, keys: CalibKeys) -> CalibData:
    return frozendict({k.split("_")[-1]: data[k] for k in keys})


@lru_cache(maxsize=16)
def _get_pyfai(calib: frozendict) -> AzimuthalIntegrator:
    return AzimuthalIntegrator(**calib)


@lru_cache(maxsize=16)
def _get_binner(calib: frozendict, shape: tuple):
    ai = _get_pyfai(calib)
    return generate_binner(ai, shape)


def _write_tiff(image: np.ndarray, filepath: str) -> None:
    with TiffWriter(filepath) as tw:
        tw.save(image)
    io.server_message("Save the image at '{}' for pyFAI-calib2.".format(filepath))
    return


def _run_calibration_gui(tiff_file: str, pyfai_kwargs: dict, test: bool) -> int:
    """Run the gui of calibration."""
    args = ["pyFAI-calib2"]
    _add_kwargs(args, pyfai_kwargs)
    args.append(tiff_file)
    cmd = " ".join(args)
    io.server_message("Run command 'pyFAI-calib2 {}'.".format(cmd))
    if test:
        io.server_message("Run in test mode. No interactive calibration.")
        return 0
    cp = subprocess.run(args)
    return cp.returncode


def _run_gui_in_temp(image: np.ndarray, pyfai_kwargs: dict, test: bool):
    if not ("calibrant" in pyfai_kwargs):
        io.server_message("Failed to find calibrant in start document, use Ni in default.")
        pyfai_kwargs["calibrant"] = str(ni_dspacing_file)
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        temp_tiff = temp_path.joinpath("calibration.tiff")
        _write_tiff(image, str(temp_tiff))
        returncode = _run_calibration_gui(str(temp_tiff), pyfai_kwargs, test)
    return returncode


class AnalyzerError(Exception):
    """Exception of Analyzer."""

    pass


class Analyzer(event_model.DocumentRouter):
    """The callback function to analyze the data.

    It manipulates the documents in place and return them. It add data_keys in the descriptors and update the data in the events in the primary stream. It averages the image to a 2D array and update it in place. It creates a mask for the image and adds it to data. It runs the pyFAI integration and adds the 2theta, Q, I in the data. It runs the diffpy.pdfgetx and adds the iq, sq, fq, gr arrays in the data. It obtains the maximum peak heights and positions in I(Q) and G(r) and add them in the data.

    One callback only processes one image in the data. If the name of the image is not in the data, it won't do anything. The name of the image is included in the `datakeys`.

    Parameters
    ----------
    data_keys : DataKeys
        The key names of the new data, including the object name of the detector.
    config : Config
        The configuration for the data analysis, including the parameters passed to the pyFAI and diffpy.pdfgetx.
    """

    def __init__(self, datakeys: DataKeys, default_config: Config):
        super().__init__()
        self._datakeys: DataKeys = datakeys
        self._default_config = default_config
        self._config: Config = default_config
        self._set_pdfgetter()
        self.clear_cache()

    def clear_cache(self):
        self._directories = None
        self._poni_dirs = None
        self._integration_dirs = None
        self._sq_dirs = None
        self._fq_dirs = None
        self._gr_dirs = None
        self._calib_keys: T.Optional[CalibKeys] = None
        self._calib_data: T.Optional[CalibData] = None
        self._user_mask: T.Optional[np.ndarray] = None
        self._calib_descriptor: str = ""
        self._primary_descriptor: str = ""
        self._mask_descriptor: str = ""
        self._is_calibration: bool = False
        self._pyfai_calib_kwargs: T.Optional[T.Dict] = None
        return

    def _set_and_mk_dirs(self, doc: dict) -> None:
        self._set_dirs(doc)
        self._mk_dirs()
        return

    def _set_dirs(self, doc: dict) -> None:
        if "directory" not in doc:
            raise AnalyzerError(
                "Missing key 'directory' in the doc {}".format(doc["uid"])
            )
        tiff_base = self._config.tiff_base
        self._directories: T.List[Path] = [Path(d, doc["directory"]) for d in tiff_base]
        self._poni_dirs: T.List[Path] = [d.joinpath("calib") for d in self._directories]
        self._integration_dirs: T.List[Path] = [
            d.joinpath("integration") for d in self._directories
        ]
        self._sq_dirs: T.List[Path] = [d.joinpath("sq") for d in self._directories]
        self._fq_dirs: T.List[Path] = [d.joinpath("fq") for d in self._directories]
        self._gr_dirs: T.List[Path] = [d.joinpath("gr") for d in self._directories]
        return

    def _mk_dirs(self) -> None:
        for d in self._directories:
            d.mkdir(exist_ok=True)
        for d in self._poni_dirs:
            d.mkdir(exist_ok=True)
        for d in self._integration_dirs:
            d.mkdir(exist_ok=True)
        for d in self._sq_dirs:
            d.mkdir(exist_ok=True)
        for d in self._fq_dirs:
            d.mkdir(exist_ok=True)
        for d in self._gr_dirs:
            d.mkdir(exist_ok=True)
        return

    def _set_pdfgetter(self) -> None:
        if _PDFGETX_AVAILABLE:
            pdfgetx_setting = self._config.trans_setting
            pdfconfig = PDFConfig(**pdfgetx_setting)
            self._pdfgetter = PDFGetter(pdfconfig)
            io.server_message("Create PDFGetter.")
        else:
            io.server_message("No diffpy.pdfgetx package.")
        return

    def _set_config(self, doc: dict) -> None:
        config = copy.deepcopy(self._default_config)
        config.read_user_config(doc)
        config.read_composition(doc)
        self._config = config
        return

    def _set_pyfai_calib_kwargs(self, doc: dict) -> None:
        key = self._config.pyfai_calib_kwargs
        self._is_calibration = key in doc
        self._pyfai_calib_kwargs = doc.get(key, {})
        return

    def _add_datakeys(self, doc: dict) -> None:
        keys = self._datakeys
        source = self.__class__.__name__
        object_name = "{}_{}".format(keys.detector, source)
        array_doc = {
            "dtype": "array",
            "shape": [],
            "source": source,
            "object_name": object_name,
        }
        scalar_doc = {
            "dtype": "number",
            "shape": [],
            "source": source,
            "object_name": object_name,
        }
        for k in keys.get_2d_arrays():
            doc["data_keys"][k] = array_doc
        for k in keys.get_1d_arrays():
            doc["data_keys"][k] = array_doc
        for k in keys.get_scalar():
            doc["data_keys"][k] = scalar_doc
        doc["object_keys"][object_name] = keys.get_all()
        io.server_message("Add data keys for '{}'.".format(keys.detector))
        return

    def _set_calib_keys(self, doc: dict) -> None:
        self._calib_keys = doc["object_keys"][self._datakeys.detector]
        return

    def _average_frames(self, data: dict) -> None:
        keys = self._datakeys
        dtype = self._config.image_dtype
        image: np.ndarray = np.array(data[keys.image], dtype=dtype)
        if image.ndim == 3:
            data[keys.image] = np.mean(image, axis=0, dtype=image.dtype)
            io.server_message("Average frames.")
        elif image.ndim == 2:
            io.server_message("Input frames are already averaged.")
        else:
            raise AnalyzerError(
                "'{}' has ndim = {}. Require 2 or 3.".format(keys.image, image.ndim)
            )
        return

    def _set_default(self, data: dict) -> None:
        keys = self._datakeys
        data[keys.mask] = np.zeros_like(data[keys.image], dtype=int)
        for k in keys.get_1d_arrays():
            data[k] = np.array([0.0])
        for k in keys.get_scalar():
            data[k] = 0.0
        io.server_message("Add data keys for '{}'.".format(keys.image))
        return

    def _pyfai_calibrate(self, data: dict) -> None:
        image = data[self._datakeys.image]
        pyfai_calib_kwargs = self._pyfai_calib_kwargs
        poni_file = pyfai_calib_kwargs.get("poni")
        test = self._config.is_test
        returned = _run_gui_in_temp(image, pyfai_calib_kwargs, test)
        if returned != 0:
            io.server_message("Calibration failed.")
            return
        if not poni_file:
            io.server_message("No poni file is sepcified.")
            return
        self._calib_data = _load_calib(poni_file)
        return

    def _auto_mask(
        self,
        data: dict,
        keys: DataKeys,
        user_mask: T.Optional[np.ndarray],
        calib: frozendict,
    ) -> None:
        mask_setting = self._config.mask_setting
        image = data[keys.image]
        binner = _get_binner(calib, image.shape)
        data[keys.mask] = mask_img_pyfai(image, binner, user_mask, **mask_setting)
        return

    def _update_mask(self, data: dict) -> None:
        keys = self._datakeys
        calib = self._calib_data
        assert calib is not None
        is_auto_mask = self._config.auto_mask
        user_mask = self._user_mask
        image_shape = data[keys.image].shape
        if (user_mask is not None) and (user_mask.shape != image_shape):
            io.server_message(
                "User mask shape {} != image shape {}.".format(
                    user_mask.shape, image_shape
                )
            )
            user_mask = None
        if is_auto_mask:
            self._auto_mask(data, keys, user_mask, calib)
            io.server_message("Do auto masking.")
        elif user_mask is not None:
            data[keys.mask] = user_mask
            io.server_message("Use user's mask.")
        else:
            io.server_message("No masking.")
        return

    @staticmethod
    def _get_q(tth: np.ndarray, w: float) -> np.ndarray:
        q = 4.0 * np.pi / (w * 1e10) * np.sin(np.deg2rad(tth / 2.0))
        return q

    def _update_chi(self, data: dict) -> None:
        calib = self._calib_data
        keys = self._datakeys
        ai = _get_pyfai(calib)
        integ_setting = self._config.integ_setting
        tth, intensity = ai.integrate1d(
            data[keys.image], mask=data[keys.mask], **integ_setting
        )
        data[keys.chi_2theta] = tth
        data[keys.chi_Q] = self._get_q(tth, ai.wavelength)
        data[keys.chi_I] = intensity
        idx = np.argmax(data[keys.chi_I])
        data[keys.chi_argmax] = data[keys.chi_Q][idx]
        data[keys.chi_max] = data[keys.chi_I][idx]
        io.server_message("Integrate the image.")
        return

    def _update_gr(self, data: dict) -> None:
        keys = self._datakeys
        is_pdfgetx = self._config.pdfgetx
        if not is_pdfgetx:
            io.server_message("pdfgetx = False. Skip tranformation.")
            return
        if not _PDFGETX_AVAILABLE:
            io.server_message("No diffpy.pdfgetx package. Skip transformation")
            return
        pdfgetter = self._pdfgetter
        pdfgetter(data[keys.chi_Q], data[keys.chi_I])
        data[keys.iq_Q] = data[keys.chi_Q]
        data[keys.iq_I] = data[keys.chi_I]
        data[keys.sq_Q] = pdfgetter.sq[0]
        data[keys.sq_S] = pdfgetter.sq[1]
        data[keys.fq_Q] = pdfgetter.fq[0]
        data[keys.fq_F] = pdfgetter.fq[1]
        data[keys.gr_r] = pdfgetter.gr[0]
        data[keys.gr_G] = pdfgetter.gr[1]
        idx = np.argmax(data[keys.gr_G])
        data[keys.gr_argmax] = data[keys.gr_r][idx]
        data[keys.gr_max] = data[keys.gr_G][idx]
        io.server_message("Transform the XRD to PDF.")
        return

    def _add_analyzed_data(self, data: dict) -> None:
        self._average_frames(data)
        self._set_default(data)
        if self._is_calibration:
            self._pyfai_calibrate(data)
        if self._calib_data is None:
            io.server_message("No calibration data. Skip all following steps.")
            return
        self._update_mask(data)
        self._update_chi(data)
        self._update_gr(data)
        return

    def _save_pyfai_data(self, data: dict) -> None:
        exports = self._config.exports
        calib_data = self._calib_data
        ai = _get_pyfai(calib_data)
        dks = self._datakeys
        if "poni" in exports and self._poni_dirs:
            for d in self._poni_dirs:
                poni_file = d.joinpath(data["filename"]).with_suffix(".poni")
                ai.save(poni_file)
        if "chi_2theta" in exports and self._integration_dirs:
            for d in self._integration_dirs:
                chi_tth_file = d.joinpath(data["filename"] + "_mean_tth").with_suffix(
                    ".chi"
                )
                writer = DefaultAiWriter(str(chi_tth_file), ai)
                writer.save1D(
                    str(chi_tth_file),
                    data[dks.chi_2theta],
                    data[dks.chi_I],
                    dim1_unit="2th_deg",
                )
        if "chi" in exports and self._integration_dirs:
            for d in self._integration_dirs:
                chi_q_file = d.joinpath(data["filename"] + "_mean_q").with_suffix(
                    ".chi"
                )
                writer = DefaultAiWriter(str(chi_q_file), ai)
                writer.save1D(
                    str(chi_q_file),
                    data[dks.chi_Q],
                    data[dks.chi_I],
                    dim1_unit="q_A^-1",
                )
        return

    def _save_pdfgetx_data(self, data: dict) -> None:
        exports = self._config.exports
        for key in ["sq", "fq", "gr"]:
            if key in exports:
                for d in getattr(self, f"_{key}_dirs"):
                    filename = d.joinpath(data["filename"]).with_suffix(f".{key}")
                    print(f"{d = }\n  {filename = }")
                    if getattr(self._pdfgetter, key) != (None, None):
                        self._pdfgetter.writeOutput(str(filename), key)
                    else:
                        io.server_message(f"Not saving {key} files as "
                                          f"self._pdfgetter.{key} = {getattr(self._pdfgetter, key)}")
        return

    def _save_analyzed_data(self, data: dict) -> None:
        if self._calib_data is None:
            io.server_message("No integration is done. No files output.")
            return
        if "filename" not in data:
            io.server_message("No 'filename' in data. Cannot save files.")
            return
        self._save_pyfai_data(data)
        self._save_pdfgetx_data(data)
        return

    def _set_calib_data(self, doc: dict) -> None:
        if self._calib_keys is None:
            io.server_message("No calibration data keys.")
            return
        self._calib_data = _parse_to_cailb(doc["data"], self._calib_keys)
        io.server_message("Record calibration data.")
        return

    def _set_user_mask(self, doc: dict) -> None:
        self._user_mask = np.array(doc["data"][self._datakeys.mask], dtype=np.int64)
        return

    def start(self, doc):
        self.clear_cache()
        self._set_config(doc)
        self._set_pyfai_calib_kwargs(doc)
        self._set_and_mk_dirs(doc)
        return doc

    def descriptor(self, doc):
        if doc["name"] == "primary":
            if self._datakeys.image in doc["data_keys"]:
                self._primary_descriptor = doc["uid"]
                self._add_datakeys(doc)
        elif doc["name"] == "calib":
            if self._datakeys.detector in doc["object_keys"]:
                self._calib_descriptor = doc["uid"]
                self._set_calib_keys(doc)
        elif doc["name"] == "mask":
            if self._datakeys.mask in doc["data_keys"]:
                self._mask_descriptor = doc["uid"]
        return doc

    def event(self, doc):
        if doc["descriptor"] == self._primary_descriptor:
            self._add_analyzed_data(doc["data"])
            self._save_analyzed_data(doc["data"])
        elif doc["descriptor"] == self._calib_descriptor:
            self._set_calib_data(doc)
        elif doc["descriptor"] == self._mask_descriptor:
            self._set_user_mask(doc)
        return doc

    def event_page(self, doc):
        events = []
        for event_doc in event_model.unpack_event_page(doc):
            event = self.event(event_doc)
            events.append(event)
        return event_model.pack_event_page(*events)
