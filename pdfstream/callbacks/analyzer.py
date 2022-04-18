import typing as T
from functools import lru_cache

import event_model
import numpy as np
import pdfstream.io as io
from frozendict import frozendict
from pdfstream import __version__
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.datakeys import DataKeys
from pdfstream.vend.masking import generate_binner, mask_img_pyfai
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator

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


@lru_cache(maxsize=16)
def _get_pyfai(calib: frozendict) -> AzimuthalIntegrator:
    return AzimuthalIntegrator(**calib)


@lru_cache(maxsize=16)
def _get_binner(calib: frozendict, shape: tuple):
    ai = _get_pyfai(calib)
    return generate_binner(ai, shape)


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

    def __init__(self, datakeys: DataKeys, config: Config):
        super().__init__()
        self._datakeys: DataKeys = datakeys
        self._config: Config = config
        self._calib_keys: T.Optional[CalibKeys] = None
        self._calib_data: T.Optional[CalibData] = None
        self._user_mask: T.Optional[np.ndarray] = None
        self._calib_descriptor: str = ""
        self._primary_descriptor: str = ""
        self._mask_descriptor: str = ""
        self._pdfgetter: T.Optional[PDFGetter] = None
        self._set_pdfgetter()

    def _set_pdfgetter(self) -> None:
        if _PDFGETX_AVAILABLE:
            pdfgetx_setting = self._config.trans_setting
            pdfconfig = PDFConfig(**pdfgetx_setting)
            self._pdfgetter = PDFGetter(pdfconfig)
            io.server_message("Create PDFGetter.")
        else:
            io.server_message("No diffpy.pdfgetx package.")
        return

    def _set_composition(self, doc: dict) -> None:
        key = self._config.composition_str
        if key in doc:
            composition = doc[key]
            self._pdfgetter.config.composition = composition
            io.server_message("Sample composition is '{}'.".format(composition))
        else:
            self._pdfgetter.config.composition = "Ni"
            io.server_message("No composition info. Use '{}'.".format("Ni"))
        return

    def start(self, doc):
        self._set_composition(doc)
        return doc

    def _add_datakeys(self, doc: dict) -> None:
        keys = self._datakeys
        source = self.__class__.__name__
        object_name = "{}_{}".format(keys.detector, source)
        array_doc = {
            "dtype": "array",
            "shape": [],
            "source": source,
            "object_name": object_name
        }
        scalar_doc = {
            "dtype": "number",
            "shape": [],
            "source": source,
            "object_name": object_name
        }
        for k in keys.get_2d_arrays():
            doc["data_keys"][k] = array_doc
        for k in keys.get_1d_arrays():
            doc["data_keys"][k] = array_doc
        for k in keys.get_scalar():
            doc["data_keys"][k] = scalar_doc
        doc["object_keys"][object_name] = keys.get_all()
        io.server_message(
            "Add data keys for '{}'.".format(
                keys.detector
            )
        )
        return

    def _set_calib_keys(self, doc: dict) -> None:
        self._calib_keys = doc["object_keys"][self._datakeys.detector]
        return

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

    def _average_frames(self, data: dict) -> None:
        keys = self._datakeys
        image: np.ndarray = np.array(data[keys.image])
        if image.ndim == 3:
            data[keys.image] = np.mean(image, axis=0, dtype=image.dtype)
            io.server_message("Average frames.")
        elif image.ndim == 2:
            io.server_message("Input frames are already averaged.")
        else:
            raise AnalyzerError(
                "'{}' has ndim = {}. Require 2 or 3.".format(
                    image.ndim
                )
            )
        return

    def _set_default(self, data: dict) -> None:
        keys = self._datakeys
        data[keys.mask] = np.zeros_like(data[keys.image], dtype=int)
        for k in keys.get_1d_arrays():
            data[k] = np.array([0.])
        for k in keys.get_scalar():
            data[k] = 0.
        io.server_message("Add data keys for '{}'.".format(keys.image))
        return

    def _auto_mask(
        self,
        data: dict,
        keys: DataKeys,
        user_mask: T.Optional[np.ndarray],
        calib: frozendict
    ) -> None:
        mask_setting = self._config.mask_setting
        image = data[keys.image]
        binner = _get_binner(calib, image.shape)
        data[keys.mask] = mask_img_pyfai(
            image,
            binner,
            user_mask,
            **mask_setting
        )
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
                    user_mask.shape,
                    image_shape
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
        q = 4. * np.pi / (w * 1e10) * np.sin(np.deg2rad(tth / 2.))
        return q

    def _update_chi(self, data: dict) -> None:
        calib = self._calib_data
        assert calib is not None
        keys = self._datakeys
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

    def _add_analyzed_data(self, doc: dict) -> None:
        data = doc["data"]
        self._average_frames(data)
        self._set_default(data)
        if self._calib_data is None:
            io.server_message("No calibration data. Skip all following steps.")
            return
        self._update_mask(data)
        self._update_chi(data)
        self._update_gr(data)
        return

    def _set_calib_data(self, doc: dict) -> None:
        if self._calib_keys is None:
            io.server_message("No calibration data keys.")
            return
        data = doc["data"]
        self._calib_data = frozendict(
            {
                k.split('_')[-1]: data[k]
                for k in self._calib_keys
            }
        )
        io.server_message("Record calibration data.")
        return

    def _set_user_mask(self, doc: dict) -> None:
        self._user_mask = doc["data_keys"][self._datakeys.mask]

    def event(self, doc):
        if doc["descriptor"] == self._primary_descriptor:
            self._add_analyzed_data(doc)
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

    def stop(self, doc):
        io.server_message("Finish the analysis of '{}'.".format(doc["run_start"]))
        return super().stop(doc)
