"""A streaming pipeline factory."""
import event_model
import numpy as np
from bluesky.callbacks.stream import LiveDispatcher
from configparser import ConfigParser
from databroker import catalog
from diffpy.pdfgetx import PDFConfig

import pdfstream.integration as integ
import pdfstream.pipeline.from_descriptor as from_desc
import pdfstream.pipeline.from_event as from_event
import pdfstream.pipeline.from_start as from_start
import pdfstream.pipeline.units as units
import pdfstream.transformation as trans


class AnalysisConfig(ConfigParser):
    @property
    def db_name(self):
        return self.get("RAW DB", "name")

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
            "normalization_factor": section.getfloat("normalization_factor")
        }

    @property
    def pyfai_unit(self):
        return self.get("INTEGRATION SETTING", "unit")

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

    @property
    def data_keys(self):
        section = self["DATA KEYS"]
        return {
            "masked_image": section.get("masked_image"),
            "iq": section.get("iq").split(","),
            "sq": section.get("sq").split(","),
            "fq": section.get("fq").split(","),
            "gr": section.get("gr").split(",")
        }


class AnalysisStream(LiveDispatcher):
    """The secondary stream for data analysis."""

    def __init__(self, config: AnalysisConfig):
        self.config = config
        super().__init__()
        self.cache = {}
        self.db = catalog[self.config.db_name] if self.config.db_name else None

    def start(self, doc, _md=None):
        """
        Create the stream after seeing the start document

        The callback looks for the 'average' key in the start document to
        configure itself.
        """
        # the input node
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
        super().start(doc)

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
        """Send an Event through the stream"""
        raw_img = from_event.get_image_from_event(doc, det_name=self.cache["det_name"])
        chi, final_image, _, _, final_mask, _, _ = integ.get_chi(
            self.cache["ai"], raw_img, dk_img=self.cache["dk_img"], bg_img=None, mask=None, bg_scale=None,
            mask_setting=self.config.mask_setting, integ_setting=self.config.integ_setting,
            img_setting="OFF", plot_setting="OFF"
        )
        pdfconfig = PDFConfig(
            dataformat=units.MAP_PYFAI_TO_DATAFORMAT[self.config.pyfai_unit],
            **self.cache["bt_info"],
            **self.config.trans_setting,
            **self.config.grid_config
        )
        pdfgetter = trans.get_pdf(pdfconfig, chi, plot_setting="OFF")
        keys = self.config.data_keys
        data = {
            keys["masked_image"]: np.ma.masked_array(final_image, final_mask),
            keys["iq"][0]: pdfgetter.iq[0],
            keys["iq"][1]: pdfgetter.iq[1],
            keys["sq"][0]: pdfgetter.sq[0],
            keys["sq"][1]: pdfgetter.sq[1],
            keys["fq"][0]: pdfgetter.fq[0],
            keys["fq"][1]: pdfgetter.fq[1],
            keys["gr"][0]: pdfgetter.gr[0],
            keys["gr"][1]: pdfgetter.gr[1]
        }
        self.process_event(EventDoc(data=data, descriptor=doc["descriptor"]))

    def stop(self, doc, _md=None):
        """Delete the stream when run stops"""
        self.cache = {}
        super().stop(doc)


class EventDoc(dict):
    """A simplified event document for pipeline. It only contains two necessary key: data and descriptor."""

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
