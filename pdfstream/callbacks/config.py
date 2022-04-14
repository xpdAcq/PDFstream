import typing as T
from configparser import ConfigParser
from functools import cached_property
from pathlib import Path

import numpy as np
import pdfstream.io as io
from pdfstream.units import LABELS
from pdfstream.vend.formatters import SpecialStr

SectionDict = T.Dict[str, str]
ConfigDict = T.Dict[str, SectionDict]


def _get_vlim(image: np.ndarray) -> T.Tuple[float, float]:
    m = np.mean(image)
    std = np.std(image)
    return max(m - 2 * std, 0), m + 2 * std


def _get_set(value_str: str) -> T.Set:
    if not value_str:
        return set()
    return set(value_str.replace(" ", "").split(","))


def _get_list(value_str: str) -> T.List:
    if not value_str:
        return list()
    return list(value_str.replace(" ", "").split(","))


class Config(ConfigParser):
    """The configuration for analysis callbacks."""

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        self.add_section("DATABASE")
        self.add_section("METADATA")
        self.add_section("ANALYSIS")
        self.add_section("SUITCASE")
        self.add_section("VISUALIZATION")

    @cached_property
    def sample_name_key(self) -> str:
        return self.get("METADATA", "sample_name_key", fallback="sample_name")

    @cached_property
    def image_fields(self) -> T.List:
        v = self.get("ANALYSIS", "image_fields", fallback="pe1_image,pe2_image,dexela_image")
        return _get_list(v)

    @cached_property
    def detectors(self) -> T.List:
        v = self.get("ANALYSIS", "image_fields", fallback="pe1,pe2,dexela")
        return _get_list(v)

    @cached_property
    def auto_mask(self) -> str:
        return self.getboolean("ANALYSIS", "auto_mask", fallback=True)

    @cached_property
    def user_mask_files(self) -> set:
        v = self.get("ANALYSIS", "user_mask_files", fallback="")
        return _get_set(v)

    @cached_property
    def user_mask(self) -> T.Optional[np.ndarray]:
        if len(self.user_mask_files) == 0:
            return None
        fs = iter(self.user_mask_files)
        f0 = next(fs)
        mask = io.load_matrix_flexible(f0)
        for f in fs:
            _mask = io.load_matrix_flexible(f)
            mask += _mask
        return mask

    @cached_property
    def mask_setting(self) -> dict:
        return {
            "alpha": self.getfloat("ANALYSIS", "alpha", fallback=2.5),
            "edge": self.getint("ANALYSIS", "edge", fallback=20),
            "lower_thresh": self.getfloat("ANALYSIS", "lower_thresh", fallback=0.),
            "upper_thresh": self.getfloat("ANALYSIS", "upper_thresh", fallback=None)
        }

    @cached_property
    def integ_setting(self) -> dict:
        return {
            "npt": self.getint("ANALYSIS", "npt", fallback=3000),
            "correctSolidAngle": self.getboolean("ANALYSIS", "correctSolidAngle", fallback=False),
            "polarization_factor": self.getfloat("ANALYSIS", "polarization_factor", fallback=0.99),
            "method": self.get("ANALYSIS", "method", fallback="bbox,csr,cython"),
            "normalization_factor": self.getfloat("ANALYSIS", "normalization_factor", fallback=1.),
            "unit": "2th_deg"
        }

    @cached_property
    def trans_setting(self) -> dict:
        return {
            "rpoly": self.getfloat("ANALYSIS", "rpoly", fallback=1.2),
            "qmaxinst": self.getfloat("ANALYSIS", "qmaxinst", fallback=24.),
            "qmin": self.getfloat("ANALYSIS", "qmin", fallback=0.),
            "qmax": self.getfloat("ANALYSIS", "qmax", fallback=22.),
            "rmin": self.getfloat("ANALYSIS", "rmin", fallback=0.),
            "rmax": self.getfloat("ANALYSIS", "rmax", fallback=30.),
            "rstep": self.getfloat("ANALYSIS", "rstep", fallback=0.01),
            "composition": self.get("ANALYSIS", "composition", fallback="Ni"),
            "dataformat": "QA"
        }

    @cached_property
    def directory(self) -> str:
        return self.get("SUITCASE", "tiff_base", fallback=".")

    @cached_property
    def file_prefix(self) -> str:
        return SpecialStr(
            self.get("ANALYSIS", "file_prefix", fallback="start[uid]_"))

    @cached_property
    def pdfgetx(self) -> bool:
        return self.getboolean("ANALYSIS", "pdfgetx", fallback=True)

    @cached_property
    def raw_db(self) -> str:
        return self.get("DATABASE", "raw_db", fallback="")

    @cached_property
    def composition_key(self) -> str:
        return self.get("METADATA", "composition_key", fallback="composition_str")

    @cached_property
    def calib_identifier(self) -> str:
        return self.get("METADATA", "calib_identifier", fallback="is_calibration")

    @cached_property
    def exports(self) -> set:
        v = self.get("SUITCASE", "exports", fallback="poni,tiff,mask,yaml,csv,txt")
        return _get_set(v)

    @cached_property
    def file_prefix(self) -> SpecialStr:
        return SpecialStr(
            self.get("SUITCASE", "file_prefix", fallback="{start[original_run_uid]}_{start[readable_time]}_"))

    @cached_property
    def directory_template(self) -> SpecialStr:
        return SpecialStr(self.get("SUITCASE", "directory_template", fallback="{start[sample_name]}_data"))

    @cached_property
    def tiff_base(self) -> Path:
        """Settings for the base folder."""
        dir_path = self.get("SUITCASE", "tiff_base")
        if not dir_path:
            dir_path = "~/pdfstream_data"
            io.server_message("Missing tiff_base in configuration. Use '{}'".format(dir_path))
        path = Path(dir_path).expanduser()
        return path

    @cached_property
    def tiff_setting(self) -> dict:
        return {
            "astype": self.get("SUITCASE", "tiff_astype", fallback="float32"),
            "bigtiff": self.getboolean("SUITCASE", "tiff_bigtiff", fallback=False),
            "byteorder": self.get("SUITCASE", "tiff_byteorder", fallback=None),
            "imagej": self.get("SUITCASE", "tiff_imagej", fallback=False)
        }

    @cached_property
    def visualizers(self) -> set:
        v = self.get(
            "VISUALIZATION",
            "visualizers",
            fallback="dk_sub_image,masked_image,chi,chi_2theta,iq,sq,fq,gr,chi_max,chi_argmax,gr_max,gr_argmax"
        )
        return _get_set(v)

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

    def to_dict(self) -> ConfigDict:
        """Convert the configuration to a dictionary."""
        return {s: dict(self.items(s)) for s in self.sections()}

    def read_user_config(self, user_config: dict) -> None:
        self.read_dict({"ANALYSIS": user_config})
        return
