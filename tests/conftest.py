"""Configuration of pytest."""
import numpy
import pyFAI
import pytest
from diffpy.pdfgetx import PDFConfig, PDFGetter
from pkg_resources import resource_filename

from pdfstream.io import load_img, load_data

NI_PONI = resource_filename('tests', 'test_data/Ni_poni_file.poni')
NI_GR = resource_filename('tests', 'test_data/Ni_gr_file.gr')
NI_CHI = resource_filename('tests', 'test_data/Ni_chi_file.chi')
NI_FGR = resource_filename('tests', 'test_data/Ni_fgr_file.fgr')
NI_IMG = resource_filename('tests', 'test_data/Ni_img_file.tiff')
MASK_FILE = resource_filename("tests", "test_data/mask_file.npy")
KAPTON_IMG = resource_filename('tests', 'test_data/Kapton_img_file.tiff')
BLACK_IMG = resource_filename('tests', 'test_data/black_img.tiff')
WHITE_IMG = resource_filename('tests', 'test_data/white_img.tiff')
NI_CONFIG = PDFConfig()
NI_CONFIG.readConfig(NI_GR)
NI_PDFGETTER = PDFGetter(NI_CONFIG)

DB = {
    'Ni_img_file': NI_IMG,
    'Ni_img': load_img(NI_IMG),
    'Kapton_img_file': KAPTON_IMG,
    'Kapton_img': load_img(KAPTON_IMG),
    'Ni_poni_file': NI_PONI,
    'Ni_gr_file': NI_GR,
    'Ni_chi_file': NI_CHI,
    'Ni_fgr_file': NI_FGR,
    'ai': pyFAI.load(NI_PONI),
    'Ni_gr': load_data(NI_GR).T,
    'Ni_chi': load_data(NI_CHI).T,
    'Ni_fgr': load_data(NI_FGR).T,
    'black_img_file': BLACK_IMG,
    'white_img_file': WHITE_IMG,
    'black_img': numpy.zeros((128, 128)),
    'white_img': numpy.ones((128, 128)),
    'Ni_config': NI_CONFIG,
    'Ni_pdfgetter': NI_PDFGETTER,
    'mask_file': MASK_FILE
}


@pytest.fixture(scope="session")
def db():
    return DB
