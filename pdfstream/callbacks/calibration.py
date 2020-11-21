import subprocess
import typing as tp
from configparser import Error
from pathlib import Path

import event_model
import numpy as np
from bluesky.callbacks.core import CallbackBase
from tifffile import TiffWriter

import pdfstream.callbacks.from_descriptor as fd
import pdfstream.callbacks.from_event as fe
import pdfstream.callbacks.from_start as fs
from .analysis import BasicAnalysisConfig, BasicExportConfig


class CalibrationConfig(BasicAnalysisConfig, BasicExportConfig):
    """The configuration of the calibration callbacks."""

    @property
    def calib_identifier(self):
        return self.get("METADATA", "calib_identifier")

    @property
    def default_calibrant(self):
        return self.get("CALIBRATION", "default_calibrant")

    @property
    def detector_key(self):
        return self.get("METADATA", "detector_key")

    @property
    def calibrant_key(self):
        return self.get("METADATA", "calibrant_key")

    @property
    def calib_base(self):
        dir_path = self.get("FILE SYSTEM", "calib_base")
        if not dir_path:
            raise Error("Missing calib_base in configuration.")
        path = Path(dir_path).expanduser()
        return path

    @calib_base.setter
    def calib_base(self, value: str):
        self.set("FILE SYSTEM", "calib_base", value)

    @property
    def calib_tiff_dir(self):
        dir_path = self.tiff_base.joinpath("calib")
        return dir_path

    @property
    def poni_file(self):
        return self.get("CALIBRATION", "poni_file")


class Calibration(CallbackBase):
    """Run the calibration in a gui and save the results which will be used by xpdacq."""

    def __init__(self, config: CalibrationConfig, *, test: bool = False):
        super(Calibration, self).__init__()
        self.config = config
        self.cache = dict()
        self.db = self.config.raw_db
        self.test = test

    def start(self, doc):
        super(Calibration, self).start(doc)
        self.cache = dict()
        self.cache["img_sum"] = 0
        self.cache["img_num"] = 0
        self.cache["start"] = doc
        self.cache["calib_info"] = fs.get_calib_info(
            doc,
            wavelength_key=self.config.wavelength_key,
            detector_key=self.config.detector_key,
            calibrant_key=self.config.calibrant_key
        )

    def descriptor(self, doc):
        super(Calibration, self).descriptor(doc)
        self.cache["det_name"] = fd.find_one_image(doc)
        self.cache["dk_img"] = fs.query_dk_img(
            self.cache["start"],
            db=self.db,
            dk_id_key=self.config.dk_id_key,
            det_name=self.cache["det_name"]
        )

    def event_page(self, doc):
        for event_doc in event_model.unpack_event_page(doc):
            self.event(event_doc)

    def event(self, doc):
        super(Calibration, self).event(doc)
        raw_img = fe.get_image_from_event(doc, self.cache["det_name"])
        self.cache["img_sum"] += raw_img
        self.cache["img_num"] += 1

    def stop(self, doc):
        super(Calibration, self).stop(doc)
        self.config.calib_base.mkdir(parents=True, exist_ok=True)
        self.config.calib_tiff_dir.mkdir(parents=True, exist_ok=True)
        poni_path = self.config.calib_base.joinpath(self.config.poni_file)
        tiff_path = self.config.calib_tiff_dir.joinpath("{}-calib.tiff".format(self.cache["start"]["uid"]))
        calc_image_and_save(
            self.cache["img_sum"],
            self.cache["img_num"],
            self.cache["dk_img"],
            tiff_path
        )
        run_calibration_gui(
            tiff_path,
            poni_path,
            **self.cache["calib_info"],
            test=self.test
        )
        self.cache = dict()


def calc_image_and_save(img_sum: np.ndarray, img_num: int, dk_img: tp.Union[None, np.ndarray],
                        tiff_path: tp.Union[str, Path]) -> None:
    """Average the image, subtract the dark image and export the image in a tiff file."""
    avg_img = img_sum / img_num
    if dk_img is not None:
        avg_img = avg_img - dk_img
    tw = TiffWriter(tiff_path)
    tw.write(avg_img)
    return


def run_calibration_gui(
    tiff_file: Path,
    poni_file: Path,
    *,
    wavelength: float = "",
    calibrant: str = "",
    detector: str = "",
    test: bool = False
) -> int:
    """Run the gui of calibration."""
    args = ["pyFAI-calib2", "--poni", str(poni_file)]
    if wavelength:
        args.extend(["--wavelength", wavelength])
    if calibrant:
        args.extend(["--calibrant", calibrant])
    if detector:
        args.extend(["--detector", detector])
    args.append(str(tiff_file))
    if test:
        return 0
    cp = subprocess.run(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return cp.returncode
