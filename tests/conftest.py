"""Configuration of pytest."""
import json
import multiprocessing
import time
import uuid
from pathlib import Path

import databroker
import matplotlib.pyplot as plt
import numpy
import numpy as np
import pyFAI
import pytest
from bluesky.callbacks.zmq import Proxy
from databroker.v2 import Broker
from diffpy.pdfgetx import PDFConfig, PDFGetter
from pkg_resources import resource_filename

from pdfstream.callbacks.composer import gen_stream
from pdfstream.io import load_img, load_array

plt.ioff()

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
    'mask': MASK
}


@pytest.fixture(scope="session")
def test_data():
    """Test configs."""
    return DB


def start_proxy():
    Proxy(5567, 5568).start()


@pytest.fixture(scope="session")
def proxy():
    proxy_proc = multiprocessing.Process(target=start_proxy, daemon=True)
    proxy_proc.start()
    time.sleep(4)  # Give this plenty of time to start up.
    yield "127.0.0.1:5567", "127.0.0.1:5568"
    proxy_proc.terminate()
    proxy_proc.join()


@pytest.fixture(scope="function")
def simple_stream():
    return gen_stream([{"pe1_image": NI_IMG}], START_DOC)


@pytest.fixture(scope="session")
def db_with_dark_and_light() -> Broker:
    """A database with a dark run and a light run inside. The last one is light and the first one is dark."""
    db = databroker.v2.temp()
    dark_data = [{"pe1_image": np.zeros_like(NI_IMG)}]
    dark_uid = str(uuid.uuid4())
    for name, doc in gen_stream(dark_data, {"dark_frame": True}, uid=dark_uid):
        db.v1.insert(name, doc)
    light_data = [{"pe1_image": NI_IMG}]
    for name, doc in gen_stream(light_data, dict(**START_DOC, sc_dk_field_uid=dark_uid)):
        db.v1.insert(name, doc)
    return db


@pytest.fixture(scope="session")
def db_with_dark_and_scan() -> Broker:
    """A database with a dark run and a motor scan inside. The last one is light and the first one is dark."""
    db = databroker.v2.temp()
    dark_data = [{"pe1_image": np.zeros_like(NI_IMG)}]
    dark_uid = str(uuid.uuid4())
    for name, doc in gen_stream(dark_data, {"dark_frame": True}, uid=dark_uid):
        db.v1.insert(name, doc)
    light_data = [
        {"pe1_image": NI_IMG, "temperature": 0},
        {"pe1_image": NI_IMG, "temperature": 1},
        {"pe1_image": NI_IMG, "temperature": 3}
    ]
    start = dict(**START_DOC, sc_dk_field_uid=dark_uid)
    start.update({"hints": {"dimensions": [(["temperature"], "primary")]}})
    for name, doc in gen_stream(light_data, start):
        db.v1.insert(name, doc)
    return db


@pytest.fixture(scope="session")
def db_with_dark_and_calib() -> Broker:
    """A database with a dark run and a light run inside. The last one is light and the first one is dark."""
    db = databroker.v2.temp()
    dark_data = [{"pe1_image": np.zeros_like(NI_IMG)}]
    dark_uid = str(uuid.uuid4())
    for name, doc in gen_stream(dark_data, {"dark_frame": True}, uid=dark_uid):
        db.v1.insert(name, doc)
    light_data = [{"pe1_image": NI_IMG}]
    for name, doc in gen_stream(
        light_data, dict(
            sample_composition="Ni",
            sc_dk_field_uid=dark_uid,
            detector="perkin_elmer",
            calibration=True,
            bt_wavelength=0.1917
        )
    ):
        db.v1.insert(name, doc)
    return db
