import datetime
import shutil
import subprocess
import typing as tp
from pathlib import Path

import event_model
import numpy as np
from bluesky.callbacks.stream import LiveDispatcher
from databroker.v1 import Broker
from tifffile import TiffWriter

import pdfstream
import pdfstream.callbacks.analysis as an
import pdfstream.callbacks.from_descriptor as fd
import pdfstream.callbacks.from_event as fe
import pdfstream.callbacks.from_start as fs
import pdfstream.io as io
from pdfstream.errors import ValueNotFoundError
from .analysis import AnalysisConfig


class CalibrationConfig(AnalysisConfig):
    """The configuration of the calibration callbacks."""

    def __init__(self, *args, **kwargs):
        super(CalibrationConfig, self).__init__(*args, **kwargs)
        self.add_section("CALIBRATION")

    @property
    def calib_identifier(self):
        return self.get("METADATA", "calib_identifier", fallback="is_calibration")

    @property
    def default_calibrant(self):
        return self.get("CALIBRATION", "default_calibrant", fallback="Ni")

    @property
    def detector_key(self):
        return self.get("METADATA", "detector_key", fallback="detector")

    @property
    def calibrant_key(self):
        return self.get("METADATA", "calibrant_key", fallback="sample_composition")

    @property
    def calib_base(self):
        dir_path = self.get("CALIBRATION", "calib_base")
        if not dir_path:
            dir_path = "~/pdfstream_calibration"
            io.server_message("Missing calib_base in configuration. Use '{}'.".format(dir_path))
        return Path(dir_path).expanduser()

    @calib_base.setter
    def calib_base(self, value: str):
        self.set("CALIBRATION", "calib_base", value)

    @property
    def poni_file(self):
        return self.get("CALIBRATION", "poni_file", fallback="xpdAcq_calib_info.poni")


class Calibration(LiveDispatcher):
    """Run the calibration in a gui and save the results which will be used by xpdacq."""

    def __init__(self, config: CalibrationConfig, *, test: bool = False):
        super(Calibration, self).__init__()
        self.config = config
        self.cache = dict()
        raw_db = self.config.raw_db
        self.db = Broker.named(raw_db) if raw_db else None
        self.test = test
        self.start_doc = {}
        self.event_doc = {}
        self.dirc = None
        self.file_prefix = None

    def start(self, doc, **kwargs):
        self.start_doc = doc
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
        self.cache["det_name"] = fd.find_one_image(doc)
        io.server_message("Calibrate the detector '{}'.".format(self.cache["det_name"]))
        try:
            self.cache["dk_img"] = fs.query_dk_img(
                self.cache["start"],
                db=self.db,
                dk_id_key=self.config.dk_id_key,
                det_name=self.cache["det_name"]
            )
        except ValueNotFoundError as error:
            self.cache["dk_img"] = None
            io.server_message("Failed to find dark: " + str(error))
        return super(Calibration, self).descriptor(doc)

    def event_page(self, doc):
        for event_doc in event_model.unpack_event_page(doc):
            self.event(event_doc, )

    def event(self, doc, **kwargs):
        self.event_doc = doc
        raw_img = fe.get_image_from_event(doc, self.cache["det_name"])
        self.cache["img_sum"] += raw_img
        self.cache["img_num"] += 1

    def stop(self, doc, **kwargs):
        self.config.calib_base.mkdir(parents=True, exist_ok=True)
        poni_path = self.config.calib_base.joinpath(self.config.poni_file)
        tiff_path = self.config.calib_base.joinpath("{}-calib.tiff".format(self.cache["start"]["uid"]))
        avg_img = np.divide(self.cache["img_sum"], self.cache["img_num"])
        dk_img = self.cache["dk_img"]
        calc_image_and_save(
            avg_img,
            dk_img,
            tiff_path
        )
        io.server_message("Run pyFAI-calib2 on the image '{}'.".format(str(tiff_path)))
        run_calibration_gui(
            tiff_path,
            poni_path,
            **self.cache["calib_info"],
            test=self.test
        )
        shutil.rmtree(tiff_path, ignore_errors=True)
        if self.test:
            return
        # emit start
        io.server_message("Process the data using the calibration.")
        ai = io.load_ai_from_poni_file(str(poni_path))
        new_start = dict(
            **self.start_doc,
            an_config=self.config.to_dict(),
            pdfstream_version=pdfstream.__version__
        )
        new_start[self.config.calibration_md_key] = ai.getPyFAI()
        bt_info = fs.query_bt_info(
            new_start,
            composition_key=self.config.composition_key,
            wavelength_key=self.config.wavelength_key
        )
        new_start["hints"] = {'dimensions': [[['time'], 'primary']]}
        # inject readable time
        new_start["readable_time"] = datetime.datetime.fromtimestamp(doc["time"]).strftime(
            "%Y%m%d-%H%M%S")
        # add sample_name and if it is not there
        new_start.setdefault("sample_name", "unnamed_sample")
        new_start.setdefault("original_run_uid", doc["uid"])
        # emit
        super(Calibration, self).start(new_start)
        # get the filename of the gr, sq, fq
        d = self.config.directory
        self.dirc = Path(d).expanduser().joinpath(new_start["sample_name"])
        self.dirc.mkdir(parents=True, exist_ok=True)
        # create file prefix
        fp = self.config.file_prefix
        self.file_prefix = fp.format(start=new_start)
        filename = self.file_prefix + "0001"
        # emit descriptor and event
        data = an.process(
            raw_img=avg_img,
            ai=ai,
            dk_img=dk_img,
            integ_setting=self.config.integ_setting,
            pdfgetx_setting=dict(**self.config.trans_setting, **bt_info),
            mask_setting=self.config.mask_setting,
            filename=filename,
            directory=str(self.dirc)
        )
        io.server_message("Emit the processed data.")
        super(Calibration, self).process_event({"data": data, "descriptor": self.event_doc["descriptor"]})
        # emit stop
        self.cache = dict()
        return super(Calibration, self).stop(doc)


def calc_image_and_save(avg_img: np.ndarray, dk_img: tp.Union[None, np.ndarray],
                        tiff_path: tp.Union[str, Path]) -> None:
    """Average the image, subtract the dark image and export the image in a tiff file."""
    if dk_img is not None:
        avg_img = avg_img - dk_img
    tw = TiffWriter(tiff_path)
    tw.write(avg_img)
    return


def run_calibration_gui(
        tiff_file: Path,
        poni_file: Path,
        *,
        wavelength: str = "",
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
    if cp.returncode != 0:
        io.server_message("Error in Calibration. See below:")
        print(r"$", " ".join(args))
        print(cp.stdout.decode())
        print(cp.stderr.decode())
    return cp.returncode
