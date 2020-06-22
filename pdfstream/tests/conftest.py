"""Configuration of pytest."""
import numpy
import pyFAI
import pytest
from pkg_resources import resource_filename
from pyobjcryst import loadCrystal

from pdfstream.io import load_img
from pdfstream.transformation import __PDFGETX_AVAL__
from pdfstream.utils.data import load_data

NI_PONI = resource_filename('pdfstream', 'test_data/Ni_poni_file.poni')
NI_GR = resource_filename('pdfstream', 'test_data/Ni_gr_file.gr')
NI_CHI = resource_filename('pdfstream', 'test_data/Ni_chi_file.chi')
NI_FGR = resource_filename('pdfstream', 'test_data/Ni_fgr_file.fgr')
NI_IMG = resource_filename('pdfstream', 'test_data/Ni_img_file.tiff')
NI_CIF = resource_filename('pdfstream', 'test_data/Ni_cif_file.cif')
KAPTON_IMG = resource_filename('pdfstream', 'test_data/Kapton_img_file.tiff')
BLACK_IMG = resource_filename('pdfstream', 'test_data/black_img.tiff')
WHITE_IMG = resource_filename('pdfstream', 'test_data/white_img.tiff')
if __PDFGETX_AVAL__:
    from diffpy.pdfgetx import PDFConfig

    NI_CONFIG = PDFConfig()
    NI_CONFIG.readConfig(NI_GR)
else:
    NI_CONFIG = None

DB = {
    'Ni_img_file': NI_IMG,
    'Ni_img': load_img(NI_IMG),
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
    'Ni_config': NI_CONFIG,
    'Ni_stru_file': NI_CIF,
    'Ni_stru': loadCrystal(NI_CIF)
}


@pytest.fixture
def db():
    return DB
