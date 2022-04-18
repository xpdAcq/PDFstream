import typing as T
import json
from configparser import ConfigParser
from functools import cached_property
from pathlib import Path
from typing_extensions import Self

import numpy as np
import pdfstream.io as io
from pdfstream.units import LABELS
from pdfstream.vend.formatters import SpecialStr

SectionDict = T.Dict[str, str]
ConfigDict = T.Dict[str, SectionDict]
DEFAULT_CONFIGURE = {
    "METADATA": {
        "composition_str": "composition_str",
        "sample_name": "sample_name",
        "user_config": "user_config"
    },
    "ANALYSIS": {
        "detectors": json.dumps(['pe1', 'pe2', 'dexela']),
        "image_fields": json.dumps(['pe1_image', 'pe2_image', 'dexela_image']),
        "auto_mask": "True",
        "alpha": "2.0",
        "edge": "20",
        "lower_thresh": "0.0",
        "upper_thresh": json.dumps(None),
        "npt": "3000",
        "correctSolidAngle": "False",
        "polarization_factor": "0.99",
        "method": "bbox,csr,cython",
        "normalization_factor": "1.",
        "pdfgetx": "True",
        "rpoly": "1.2",
        "qmaxinst": "24.0",
        "qmax": "22.0",
        "qmin": "0.0",
        "rmin": "0.0",
        "rmax": "30.0",
        "rstep": "0.01",
        "composition": "Ni",
        "exports": json.dumps(['yaml', 'poni', 'tiff', 'mask', 'csv', 'pyfai', 'pdfgetx']),
        "tiff_base": "~/acqsim/xpdUser/tiff_base",
        "directory": "{sample_name}",
        "file_prefix": "{sample_name}_",
        "additional_hints": json.dumps(None)
    },
    "VISUALIZATION": {
        "visualizers": json.dumps(['image', 'masked_image', 'chi_2theta', 'chi', 'iq', 'sq', 'fq', 'gr', 'qoi']),
    },
    "PROXY": {
        "inbound_address": "localhost:5567",
        "outbound_address": "localhost:5568",
        "raw_data_prefix": "raw",
        "analyzed_data_prefix": "an"
    }
}


def _get_vlim(image: np.ndarray) -> T.Tuple[float, float]:
    m = np.mean(image)
    std = np.std(image)
    return max(m - 2 * std, 0), m + 2 * std


class Config(ConfigParser):
    """The configuration for analysis callbacks."""

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.read_dict(DEFAULT_CONFIGURE)

    @cached_property
    def is_calibration(self) -> str:
        return self.get("METADATA", "is_calibration")

    @cached_property
    def composition_str(self) -> str:
        return self.get("METADATA", "composition_str")

    @cached_property
    def sample_name(self) -> str:
        return self.get("METADATA", "sample_name")

    @cached_property
    def user_config(self) -> str:
        return self.get("METADATA", "user_config")

    @cached_property
    def image_fields(self) -> T.List:
        return json.loads(self.get("ANALYSIS", "image_fields"))

    @cached_property
    def detectors(self) -> T.List:
        return json.loads(self.get("ANALYSIS", "detectors"))

    @cached_property
    def auto_mask(self) -> str:
        return self.getboolean("ANALYSIS", "auto_mask", fallback=True)

    @cached_property
    def mask_setting(self) -> dict:
        return {
            "alpha": self.getfloat("ANALYSIS", "alpha"),
            "edge": self.getint("ANALYSIS", "edge"),
            "lower_thresh": self.getfloat("ANALYSIS", "lower_thresh"),
            "upper_thresh": json.loads(self.get("ANALYSIS", "upper_thresh"))
        }

    @cached_property
    def integ_setting(self) -> dict:
        return {
            "npt": self.getint("ANALYSIS", "npt"),
            "correctSolidAngle": self.getboolean("ANALYSIS", "correctSolidAngle"),
            "polarization_factor": self.getfloat("ANALYSIS", "polarization_factor"),
            "method": self.get("ANALYSIS", "method"),
            "normalization_factor": self.getfloat("ANALYSIS", "normalization_factor"),
            "unit": "2th_deg"
        }

    @cached_property
    def trans_setting(self) -> dict:
        return {
            "rpoly": self.getfloat("ANALYSIS", "rpoly"),
            "qmaxinst": self.getfloat("ANALYSIS", "qmaxinst"),
            "qmin": self.getfloat("ANALYSIS", "qmin"),
            "qmax": self.getfloat("ANALYSIS", "qmax"),
            "rmin": self.getfloat("ANALYSIS", "rmin"),
            "rmax": self.getfloat("ANALYSIS", "rmax"),
            "rstep": self.getfloat("ANALYSIS", "rstep"),
            "composition": self.get("ANALYSIS", "composition"),
            "dataformat": "QA"
        }

    @cached_property
    def pdfgetx(self) -> bool:
        return self.getboolean("ANALYSIS", "pdfgetx")

    @cached_property
    def exports(self) -> set:
        return set(json.loads(self.get("ANALYSIS", "exports")))

    @cached_property
    def tiff_base(self) -> Path:
        """Settings for the base folder."""
        return Path(self.get("ANALYSIS", "tiff_base")).expanduser()

    @cached_property
    def directory(self) -> SpecialStr:
        return SpecialStr(self.get("ANALYSIS", "directory"))

    @cached_property
    def file_prefix(self) -> str:
        return SpecialStr(self.get("ANALYSIS", "file_prefix"))

    @cached_property
    def tiff_setting(self) -> dict:
        return {
            "astype": self.get("ANALYSIS", "tiff_astype", fallback="float32"),
            "bigtiff": self.getboolean("ANALYSIS", "tiff_bigtiff", fallback=False),
            "byteorder": self.get("ANALYSIS", "tiff_byteorder", fallback=None),
            "imagej": self.get("ANALYSIS", "tiff_imagej", fallback=False)
        }

    @cached_property
    def visualizers(self) -> set:
        return set(json.loads(self.get("VISUALIZATION", "visualizers")))

    @cached_property
    def vis_masked_image(self) -> dict:
        return {
            "cmap": "viridis",
            "limit_func": _get_vlim
        }

    @cached_property
    def vis_dk_sub_image(self) -> dict:
        return {
            "cmap": "viridis",
            "limit_func": _get_vlim
        }

    @cached_property
    def vis_2theta(self) -> dict:
        return {
            "xlabel": LABELS.tth[0],
            "ylabel": LABELS.tth[1]
        }

    @cached_property
    def vis_chi(self) -> dict:
        return {
            "xlabel": LABELS.chi[0],
            "ylabel": LABELS.chi[1]
        }

    @cached_property
    def vis_iq(self) -> dict:
        return {
            "xlabel": LABELS.iq[0],
            "ylabel": LABELS.iq[1]
        }

    @cached_property
    def vis_sq(self) -> dict:
        return {
            "xlabel": LABELS.sq[0],
            "ylabel": LABELS.sq[1]
        }

    @cached_property
    def vis_fq(self) -> dict:
        return {
            "xlabel": LABELS.fq[0],
            "ylabel": LABELS.fq[1]
        }

    @cached_property
    def vis_gr(self) -> dict:
        return {
            "xlabel": LABELS.gr[0],
            "ylabel": LABELS.gr[1]
        }

    @cached_property
    def inbound_address(self):
        return self.get("PROXY", "inbound_address")

    @cached_property
    def outbound_address(self):
        return self.get("PROXY", "outbound_address")

    @cached_property
    def raw_data_prefix(self):
        return self.get("PROXY", "raw_data_prefix").encode()

    @cached_property
    def analyzed_data_prefix(self):
        return self.get("PROXY", "analyzed_data_prefix").encode()

    def to_dict(self) -> ConfigDict:
        """Convert the configuration to a dictionary."""
        return {s: dict(self.items(s)) for s in self.sections()}

    def read_user_config(self, doc: dict) -> None:
        """Read the user configuration from the start document. It only changes the ANALSIS section."""
        user_config = doc.get(self.user_config, {})
        user_config = {str(k): json.dumps(v) for k, v in user_config.items()}
        self.read_dict({"ANALYSIS": user_config})
        return

    def read_composition(self, doc: dict) -> None:
        """Read composition string from the start docment."""
        key = self.composition_str
        if key in doc:
            composition = doc[key]
            self.set("ANALYSIS", "composition", composition)
            io.server_message("Sample composition is '{}'.".format(composition))
        else:
            io.server_message("No '{}' in the start document.".format(key))
        return
