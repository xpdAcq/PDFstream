import matplotlib.pyplot as plt

from pdfstream.transformation.main import get_pdf


def test_get_pdf(db):
    get_pdf(db['Ni_config'], db['Ni_chi'])
    plt.close()
