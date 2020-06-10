"""Configuration of pytest."""
import numpy
import pyFAI
import pytest
from diffpy.pdfgetx import PDFConfig
from pkg_resources import resource_filename

from pdfstream.utils.data import load_data

NI_PONI = resource_filename('pdfstream', 'test_data/Ni_poni_file.poni')
NI_GR = resource_filename('pdfstream', 'test_data/Ni_gr_file.gr')
NI_CHI = resource_filename('pdfstream', 'test_data/Ni_chi_file.chi')
NI_FGR = resource_filename('pdfstream', 'test_data/Ni_fgr_file.fgr')
NI_IMG = resource_filename('pdfstream', 'test_data/Ni_img_file.tiff')
KAPTON_IMG = resource_filename('pdfstream', 'test_data/Kapton_img_file.tiff')
BLACK_IMG = resource_filename('pdfstream', 'test_data/black_img.tiff')
WHITE_IMG = resource_filename('pdfstream', 'test_data/white_img.tiff')
NI_CONFIG = PDFConfig()
NI_CONFIG.readConfig(NI_GR)

DB = {
    'Ni_img_file': NI_IMG,
    'Kapton_img_file': KAPTON_IMG,
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
    'Ni_config': NI_CONFIG
}


@pytest.fixture
def db():
    return DB
