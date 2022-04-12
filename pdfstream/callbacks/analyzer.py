import copy
import datetime
import typing as tp
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import event_model
import numpy as np
import pdfstream.io as io
from frozendict import frozendict
from pdfstream import __version__
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.datakeys import DataKeys
from pdfstream.callbacks.livedispatcher import LiveDispatcher
from pdfstream.vend.masking import generate_binner, mask_img_pyfai
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator

try:
    from diffpy.pdfgetx import PDFConfig, PDFGetter

    _PDFGETX_AVAILABLE = True
except ImportError:
    _PDFGETX_AVAILABLE = False

Keys = tp.List[str]
Data = tp.Dict[str, tp.Any]
Units = tp.List[str]
DeviceName = str
CalibData = dict
CalibCahce = tp.Dict[DeviceName, CalibData]


@lru_cache(maxsize=16)
def _get_pyfai(calib: frozendict) -> AzimuthalIntegrator:
    return AzimuthalIntegrator(**calib)


@lru_cache(maxsize=16)
def _get_binner(calib: frozendict, shape: tuple):
    ai = _get_pyfai(calib)
    return generate_binner(ai, shape)


class Analyzor(LiveDispatcher):
    """The callback function to analyze the data.

    The analysis includes filename composition, automasking, integration and transformation.
    The analyzed data will be emitted out to the subscribers of this callback.
    """

    def __init__(self, config: Config):
        super(Analyzor, self).__init__()
        self._init_config = config
        self._config: tp.Union[Config, None] = None
        self._calib_cache: CalibCahce = defaultdict(CalibData)
        self._calib_descriptor: str = ""
        self._primary_descriptor: str = ""
        self._hints: Keys = list()
        self._units: Units = list()
        self._dirctory: tp.Optional[Path] = None
        self._rendered_prefix: str = ""
        self._pdfgetter: tp.Optional[PDFGetter] = None

    def _set_config(self, doc: dict) -> None:
        self._config = copy.deepcopy(self._init_config)
        self._config.read_user_config(doc.get("user_config", {}))
        return

    def _set_hints(self, doc: dict) -> None:
        hints = []
        dims = doc.get("hints", {}).get("dimensions", [])
        for data_keys, stream_name in dims:
            if stream_name == "primary":
                hints.extend(data_keys)
        self._hints = hints
        io.server_message("The hints are '{}'.".format(hints))
        return

    def _set_composition(self, doc: dict) -> None:
        key = self._config.composition_key
        if key in doc:
            self._config.composition = doc[key]
            io.server_message("Sample composition is '{}'.".format(doc[key]))
        else:
            io.server_message("No composition info. Use '{}'.".format(self._config.composition))
        return

    def _set_pdfgetter(self, doc: dict) -> None:
        if _PDFGETX_AVAILABLE:
            self._set_composition(doc)
            pdfgetx_setting = self._config.trans_setting
            pdfconfig = PDFConfig(**pdfgetx_setting)
            self._pdfgetter = PDFGetter(pdfconfig)
            io.server_message("Create PDFGetter.")
        else:
            io.server_message("No diffpy.pdfgetx package.")
        return

    def _compose_new_start(self, doc: dict) -> dict:
        new_start = dict(doc)
        new_start["an_config"] = self._config.to_dict(),
        new_start["pdfstream_version"] = __version__
        new_start.setdefault("sample_name", "unnamed_sample")
        new_start.setdefault("original_run_uid", doc["uid"])
        io.server_message("New start document is composed.")
        return new_start

    def _render_file_prefix(self, doc: dict) -> None:
        file_prefix = self._config.file_prefix
        self._rendered_prefix = file_prefix.format(start=doc)
        io.server_message("Render file prefix.")
        return

    def start(self, doc):
        io.server_message("Start analysis of '{}'.".format(doc["uid"]))
        self._set_config(doc)
        self._set_hints(doc)
        self._set_pdfgetter(doc)
        self._render_file_prefix(doc)
        new_start = self._compose_new_start(doc)
        return super().start(new_start)

    def _set_units(self, doc: dict) -> None:
        data_keys = doc.get("data_keys", {})
        self._units = [
            data_keys.get(k, {}).get("units", "")
            for k in self._hints
        ]
        io.server_message("The units of the hints are obtained.")
        return

    def descriptor(self, doc):
        if doc["name"] == "primary":
            self._primary_descriptor = doc["uid"]
            self._set_units(doc)
        elif doc["name"] == "calib":
            self._calib_descriptor = doc["uid"]
        return super(Analyzor, self).descriptor(doc)

    def _yield_data_keys(self, doc: dict) -> tp.Generator[DataKeys, None, None]:
        image_keys = self._config.image_keys
        data: Data = doc["data"]
        for k in data:
            if k in image_keys:
                yield DataKeys(k)
        io.server_message(
            "Find '{}' in data.".format(
                ", ".join(image_keys)
            )
        )
        return

    def _get_timestamp(self, doc: dict) -> str:
        return datetime.datetime.fromtimestamp(
            doc["time"]
        ).strftime(
            "%Y%m%d-%H%M%S"
        )

    def _get_hints_str(self, doc: dict) -> str:
        hints = self._hints
        units = self._units
        data = doc["data"]
        stack = []
        for hint, unit in zip(hints, units):
            if hint in data:
                value = data[hint]
                if isinstance(value, float):
                    s = "{}_{:.2f}{}".format(hint, value, unit).replace(".", ",")
                elif isinstance(value, int):
                    s = "{}_{}{}".format(hint, value, unit)
                else:
                    s = "{}_{}".format(hint, value)
                stack.append(s)
        return '_'.join(stack)

    def _get_numstamp(self, doc: dict) -> str:
        return "{:04d}".format(doc["seq_num"])

    def _get_rendered_middle(self, doc: dict) -> str:
        t = self._get_timestamp(doc)
        h = self._get_hints_str(doc)
        n = self._get_numstamp(doc)
        return '_'.join([t, h, n])

    def _get_filename(self, doc: dict) -> str:
        p = self._rendered_prefix
        m = self._get_rendered_middle(doc)
        filename = p + m
        io.server_message("The filename will be '{}'.".format(filename))
        return filename

    def _set_default(self, data: dict, keys: DataKeys) -> None:
        data[keys.mask] = np.zeros_like(data[keys.image], dtype=int)
        arr = np.array([0.])
        data[keys.chi_2theta] = arr
        data[keys.chi_Q] = arr
        data[keys.chi_I] = arr
        data[keys.chi_argmax] = 0.
        data[keys.chi_max] = 0.
        data[keys.iq_Q] = arr
        data[keys.iq_I] = arr
        data[keys.sq_Q] = arr
        data[keys.sq_I] = arr
        data[keys.fq_Q] = arr
        data[keys.fq_I] = arr
        data[keys.gr_r] = arr
        data[keys.gr_G] = arr
        data[keys.gr_argmax] = 0.
        data[keys.gr_max] = 0.
        io.server_message("Add data keys for '{}'.".format(keys.image))
        return

    def _get_calib(self, detector: str) -> tp.Optional[frozendict]:
        calib_cache = self._calib_cache
        if detector not in calib_cache:
            return None
        return calib_cache[detector]

    def _auto_mask(
        self, 
        data: dict, 
        keys: DataKeys, 
        user_mask: tp.Optional[np.ndarray],
        calib: frozendict
    ) -> None:
        mask_setting = self._config.mask_setting
        binner = _get_binner(calib)
        data[keys.mask] = mask_img_pyfai(
            data[keys.image],
            binner,
            user_mask,
            **mask_setting
        )
        return

    def _update_mask(self, data: dict, keys: DataKeys) -> None:
        is_auto_mask = self._config.auto_mask
        user_mask = self._config.user_mask
        image_shape = data[keys.image].shape
        if (user_mask is not None) and (user_mask.shape != image_shape):
            io.server_message(
                "User mask shape {} != image shape {}.".format(
                    user_mask.shape,
                    image_shape
                )
            )
            user_mask = None
        calib = self._get_calib(keys.detector)
        if is_auto_mask and (calib is not None):
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
        q = 4. * np.pi / (w * 1e10) * np.sin(np.deg2rad(tth / 2.))
        return q

    def _update_chi(self, data: dict, keys: DataKeys) -> None:
        calib = self._get_calib(keys.detector)
        if calib is None:
            io.server_message("No calibration data. Skip integration.")
            return
        ai = _get_pyfai(calib)
        integ_setting = self._config.integ_setting
        tth, intensity = ai.integrate1d(
            data[keys.image],
            mask=data[keys.mask],
            **integ_setting
        )
        data[keys.chi_2theta] = tth
        data[keys.chi_Q] = self._get_q(tth, ai.wavelength)
        data[keys.chi_I] = intensity
        idx = np.argmax(data[keys.chi_I])
        data[keys.chi_argmax] = data[keys.chi_Q][idx]
        data[keys.chi_max] = data[keys.chi_I][idx]
        io.server_message("Integrate the image.")
        return

    def _update_gr(self, data: dict, keys: DataKeys) -> None:
        calib_cache = self._calib_cache
        if keys.detector not in calib_cache:
            io.server_message("No calibration data. Skip transformation.")
            return
        is_pdfgetx = self._config.pdfgetx
        if not is_pdfgetx:
            io.server_message("pdfgetx = False. Skip tranformation.")
            return
        if not _PDFGETX_AVAILABLE:
            io.server_message("No diffpy.pdfgetx package. Skip transformation")
            return
        pdfgetter = self._pdfgetter
        pdfgetter(data[keys.chi_Q], data[keys.chi_I])
        data[keys.iq_Q] = pdfgetter.iq[0]
        data[keys.iq_I] = pdfgetter.iq[1]
        data[keys.sq_Q] = pdfgetter.sq[0]
        data[keys.sq_I] = pdfgetter.sq[1]
        data[keys.fq_Q] = pdfgetter.fq[0]
        data[keys.fq_I] = pdfgetter.fq[1]
        data[keys.gr_r] = pdfgetter.gr[0]
        data[keys.gr_G] = pdfgetter.gr[1]
        idx = np.argmax(data[keys.gr_G])
        data[keys.gr_argmax] = data[keys.gr_r][idx]
        data[keys.gr_max] = data[keys.gr_G][idx]
        io.server_message("Transform the XRD to PDF.")
        return

    def _analyze_data(self, data: dict, keys: DataKeys) -> None:
        self._set_default(data, keys)
        self._update_mask(data, keys)
        self._update_chi(data, keys)
        self._update_gr(data, keys)
        return

    def _get_analyzed_data(self, doc) -> dict:
        data = doc["data"].copy()
        data["filename"] = self._get_filename(doc)
        for keys in self._yield_data_keys(doc):
            self._analyze_data(data, keys)
        return data

    def _set_calib_cache(self, doc: dict) -> None:
        data = doc["data"]
        calib_cache = self._calib_cache
        for key, value in data.items():
            det = key.split('_')[0]
            param = key.split('_')[1]
            calib_cache[det][param] = value
        io.server_message("Record calibration data.")
        return

    def event(self, doc):
        if doc["descriptor"] == self._primary_descriptor:
            data = self._get_analyzed_data(doc)
            super().process_event(dict(data=data, descriptor=doc["descriptor"]))
        elif doc["descriptor"] == self._calib_descriptor:
            self._set_calib_cache(doc)
        return

    def event_page(self, doc):
        for event_doc in event_model.unpack_event_page(doc):
            self.event(event_doc)
        return

    def stop(self, doc):
        io.server_message("Finish the analysis of '{}'.".format(doc["run_start"]))
        return super().stop(doc)
