import matplotlib.pyplot as plt

from pdfstream.transformation import __PDFGETX_AVAL__
from pdfstream.transformation.main import *


def test_get_pdf(db):
    if __PDFGETX_AVAL__:
        get_pdf(db['Ni_config'], db['Ni_chi'])
        plt.close()
