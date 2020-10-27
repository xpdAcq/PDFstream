from configparser import ConfigParser

import event_model
import numpy as np
from bluesky.callbacks.stream import LiveDispatcher
from databroker.v2 import Broker
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator

import pdfstream.integration.tools as integ
import pdfstream.pipeline.from_descriptor as from_desc
import pdfstream.pipeline.from_event as from_event
import pdfstream.pipeline.from_start as from_start

try:
    from diffpy.pdfgetx import PDFConfig, PDFGetter
except ImportError:
    pass


class AnalysisConfig(ConfigParser):
    """The configuration for analysis pipeline."""

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
    def composition_key(self):
        return self.get("METADATA", "composition_key")

    @property
    def wavelength_key(self):
        return self.get("METADATA", "wavelength_key")

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
        return {s: dict(self.items(s)) for s in self.sections()}


class AnalysisStream(LiveDispatcher):
    """The secondary stream for data analysis.

    It inject the configuration into start document and emit processed data to the subscribers.
    """

    def __init__(self, config: AnalysisConfig, *, db: Broker = None):
        super().__init__()
        self.config = config
        self.cache = {}
        self.db = config.raw_db if db is None else db

    def start(self, doc, _md=None):
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
        for doc in event_model.unpack_event_page(doc):
            self.event(doc)

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
            pdfgetx_setting=dict(**self.cache["bt_info"], **self.config.trans_setting, **self.config.grid_config)
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
    """A simplified event document for pipeline.

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
