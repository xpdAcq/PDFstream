"""Configuration of pytest."""
import numpy
import pyFAI
import pytest
from diffpy.pdfgetx import PDFConfig
from pkg_resources import resource_filename

from pdfstream.utils.data import load_data

NI_PONI = resource_filename('pdfstream', 'data_files/Ni_calib.poni')
NI_GR = resource_filename('pdfstream', 'data_files/Ni.gr')
NI_CHI = resource_filename('pdfstream', 'data_files/Ni.chi')
NI_FGR = resource_filename('pdfstream', 'data_files/Ni.fgr')
NI_CONFIG = PDFConfig()
NI_CONFIG.readConfig(NI_GR)

DB = {
    'Ni_poni_file': NI_PONI,
    'Ni_gr_file': NI_GR,
    'Ni_chi_file': NI_CHI,
    'Ni_fgr_file': NI_FGR,
    'ai': pyFAI.load(NI_PONI),
    'Ni_gr': load_data(NI_GR).T,
    'Ni_chi': load_data(NI_CHI).T,
    'Ni_fgr': load_data(NI_FGR).T,
    'black_img': numpy.zeros((128, 128)),
    'Ni_config': NI_CONFIG
}


@pytest.fixture
def db():
    return DB
