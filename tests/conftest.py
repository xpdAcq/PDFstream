"""Configuration of pytest."""
import multiprocessing
import numpy
import pyFAI
import pytest
import time
from bluesky.callbacks.zmq import Proxy
from databroker import catalog
from diffpy.pdfgetx import PDFConfig, PDFGetter
from pkg_resources import resource_filename

from pdfstream.io import load_img, load_array

NI_PONI_FILE = resource_filename('tests', 'test_data/Ni_poni_file.poni')
NI_GR_FILE = resource_filename('tests', 'test_data/Ni_gr_file.gr')
NI_CHI_FILE = resource_filename('tests', 'test_data/Ni_chi_file.chi')
NI_FGR_FILE = resource_filename('tests', 'test_data/Ni_fgr_file.fgr')
NI_IMG_FILE = resource_filename('tests', 'test_data/Ni_img_file.tiff')
MASK_FILE = resource_filename("tests", "test_data/mask_file.npy")
KAPTON_IMG_FILE = resource_filename('tests', 'test_data/Kapton_img_file.tiff')
BLACK_IMG_FILE = resource_filename('tests', 'test_data/black_img.tiff')
WHITE_IMG_FILE = resource_filename('tests', 'test_data/white_img.tiff')
NI_IMG = load_img(NI_IMG_FILE)
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
    'mask': MASK
}


@pytest.fixture(scope="session")
def test_data():
    """Test configs."""
    return DB


@pytest.fixture(scope="session")
def db():
    """An example configs broker database."""
    return catalog["example"]


@pytest.fixture(scope="session")
def run0(db):
    """A run with calibration metadata."""
    return db['a3e64b70-c5b9-4437-80ea-ea6a7198d397']


def start_proxy():
    Proxy(5567, 5568).start()


@pytest.fixture(scope="session")
def proxy():
    proxy_proc = multiprocessing.Process(target=start_proxy, daemon=True)
    proxy_proc.start()
    time.sleep(3)  # Give this plenty of time to start up.
    yield "127.0.0.1:5567", "127.0.0.1:5568"
    proxy_proc.terminate()
    proxy_proc.join()
