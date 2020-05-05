"""Configuration of pytest."""
from pathlib import Path

import fabio

from pdfstream.utils.data import load_poni, load_data

TEST_DIR = Path(__file__).parent
NI_TIFF = str(TEST_DIR.joinpath('data', 'Ni_calib.tiff'))
NI_PONI = str(TEST_DIR.joinpath('data', 'Ni_calib.poni'))
BG_TIFF = str(TEST_DIR.joinpath('data', 'BG_zero.tiff'))
NI_GR_FILE = str(TEST_DIR.joinpath('data', 'Ni.gr'))
NI_CHI_FILE = str(TEST_DIR.joinpath('data', 'Ni.chi'))
NI_FGR_FILE = str(TEST_DIR.joinpath('data', 'Ni.fgr'))
NI_IMG = fabio.open(NI_TIFF).data
BG_IMG = fabio.open(BG_TIFF).data
NI_CALIB_RESULT = load_poni(NI_PONI)
NI_CHI = load_data(NI_CHI_FILE).T
NI_GR = load_data(NI_GR_FILE).T
NI_FGR = load_data(NI_FGR_FILE).T
