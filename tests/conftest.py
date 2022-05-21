"""Configuration of pytest."""
import json
from pathlib import Path

import bluesky.plans as bp
import matplotlib.pyplot as plt
import numpy
import pyFAI
import pytest
from databroker.v2 import Broker
from diffpy.pdfgetx import PDFConfig, PDFGetter
from pdfstream.io import load_array, load_img
from pkg_resources import resource_filename
from xpdacq.preprocessors import (CalibPreprocessor, DarkPreprocessor,
                                  ShutterConfig, ShutterPreprocessor,
                                  MaskPreprocessor)
from xpdacq.simulators import WorkSpace

# do not show any figures in test otherwise they will block the tests
plt.ioff()
# here are test data files
NI_PONI_FILE = resource_filename('tests', 'test_data/Ni_poni_file.poni')
DETEECTOR_PONI_FILE = resource_filename('tests', 'test_data/calibration_for_detector.poni')
MASK_BEAMSTOP_FILE = resource_filename('tests', 'test_data/mask_beamstop.npy')
NI_GR_FILE = resource_filename('tests', 'test_data/Ni_gr_file.gr')
NI_CHI_FILE = resource_filename('tests', 'test_data/Ni_chi_file.chi')
NI_FGR_FILE = resource_filename('tests', 'test_data/Ni_fgr_file.fgr')
NI_IMG_FILE = resource_filename('tests', 'test_data/Ni_img_file.tiff')
MASK_FILE = resource_filename("tests", "test_data/mask_file.npy")
KAPTON_IMG_FILE = resource_filename('tests', 'test_data/Kapton_img_file.tiff')
BLACK_IMG_FILE = resource_filename('tests', 'test_data/black_img.tiff')
WHITE_IMG_FILE = resource_filename('tests', 'test_data/white_img.tiff')
NI_IMG = load_img(NI_IMG_FILE)
NI_FRAMES = numpy.expand_dims(NI_IMG, 0)
KAPTON_IMG = load_img(KAPTON_IMG_FILE)
NI_GR = load_array(NI_GR_FILE)
NI_CHI = load_array(NI_CHI_FILE)
NI_FGR = load_array(NI_FGR_FILE)
NI_CONFIG = PDFConfig()
NI_CONFIG.readConfig(NI_GR_FILE)
NI_PDFGETTER = PDFGetter(NI_CONFIG)
AI = pyFAI.load(NI_PONI_FILE)
MASK = numpy.load(MASK_FILE)
BLACK_IMG = load_img(BLACK_IMG_FILE)
WHITE_IMG = load_img(WHITE_IMG_FILE)
START_DOC_FILE = resource_filename('tests', 'test_data/start.json')
with Path(START_DOC_FILE).open("r") as f:
    START_DOC = json.load(f)

DB = {
    'Ni_img_file': NI_IMG_FILE,
    'Ni_img': NI_IMG,
    'Kapton_img_file': KAPTON_IMG_FILE,
    'Kapton_img': KAPTON_IMG,
    'Ni_poni_file': NI_PONI_FILE,
    'Ni_gr_file': NI_GR_FILE,
    'Ni_chi_file': NI_CHI_FILE,
    'Ni_fgr_file': NI_FGR_FILE,
    'ai': AI,
    'Ni_gr': NI_GR,
    'Ni_chi': NI_CHI,
    'Ni_fgr': NI_FGR,
    'black_img_file': BLACK_IMG_FILE,
    'white_img_file': WHITE_IMG_FILE,
    'black_img': BLACK_IMG,
    'white_img': WHITE_IMG,
    'Ni_config': NI_CONFIG,
    'Ni_pdfgetter': NI_PDFGETTER,
    'mask_file': MASK_FILE,
    'mask': MASK,
    'start_doc': START_DOC
}


@pytest.fixture(scope="session")
def test_data():
    """Test configs."""
    return DB


@pytest.fixture(scope="session")
def local_dir() -> Path:
    _dir = Path(__file__).parent.joinpath("local/")
    _dir.mkdir(exist_ok=True)
    return _dir


@pytest.fixture(scope="session")
def db_with_new_xpdacq() -> Broker:
    ws = WorkSpace()
    # create CalibPreprocessor
    cpp0 = CalibPreprocessor(detector=ws.det)
    calib_data = cpp0.read(DETEECTOR_PONI_FILE)
    cpp0.add_calib_result({}, calib_data)
    # create DarkPreprocessor
    sc = ShutterConfig(ws.shutter, "open", "closed")
    dpp0 = DarkPreprocessor(detector=ws.det, shutter_config=sc)
    # create ShutterPreprocessor
    spp0 = ShutterPreprocessor(detector=ws.det, shutter_config=sc)
    # add preprocessors
    ws.RE.preprocessors.append(dpp0)
    ws.RE.preprocessors.append(cpp0)
    ws.RE.preprocessors.append(spp0)
    # run
    plan = bp.list_scan([ws.det], ws.eurotherm, [300., 400., 500.])
    ws.RE(plan, sample_name="Test_Sample", composition_str="Ni")
    return ws.db


@pytest.fixture(scope="session")
def db_with_mask_in_run() -> Broker:
    ws = WorkSpace()
    # create CalibPreprocessor
    cpp0 = CalibPreprocessor(detector=ws.det)
    calib_data = cpp0.read(DETEECTOR_PONI_FILE)
    cpp0.add_calib_result({}, calib_data)
    # create DarkPreprocessor
    sc = ShutterConfig(ws.shutter, "open", "closed")
    dpp0 = DarkPreprocessor(detector=ws.det, shutter_config=sc)
    # create ShutterPreprocessor
    spp0 = ShutterPreprocessor(detector=ws.det, shutter_config=sc)
    # create MaskPreprocessor
    mpp0 = MaskPreprocessor(detector=ws.det)
    mpp0.load_mask(str(MASK_BEAMSTOP_FILE))
    # add preprocessors
    ws.RE.preprocessors.append(dpp0)
    ws.RE.preprocessors.append(cpp0)
    ws.RE.preprocessors.append(mpp0)
    ws.RE.preprocessors.append(spp0)
    # run
    plan = bp.list_scan([ws.det], ws.eurotherm, [300., 400., 500.])
    ws.RE(plan, sample_name="Test_Mask", composition_str="Ni")
    return ws.db


@pytest.fixture(scope="session")
def db_with_new_calib() -> Broker:
    ws = WorkSpace()
    # create CalibPreprocessor
    cpp0 = CalibPreprocessor(detector=ws.det)
    calib_data = cpp0.read(DETEECTOR_PONI_FILE)
    cpp0.add_calib_result({}, calib_data)
    # create DarkPreprocessor
    sc = ShutterConfig(ws.shutter, "open", "closed")
    dpp0 = DarkPreprocessor(detector=ws.det, shutter_config=sc)
    # create ShutterPreprocessor
    spp0 = ShutterPreprocessor(detector=ws.det, shutter_config=sc)
    # add preprocessors
    ws.RE.preprocessors.append(dpp0)
    ws.RE.preprocessors.append(cpp0)
    ws.RE.preprocessors.append(spp0)
    # run
    plan = bp.count([ws.det])
    pyfai_calib_kwargs = {"poni": str(DETEECTOR_PONI_FILE)}
    ws.RE(plan, sample_name="Test_Sample", composition_str="Ni", pyfai_calib_kwargs=pyfai_calib_kwargs)
    return ws.db
