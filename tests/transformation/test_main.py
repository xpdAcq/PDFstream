import matplotlib.pyplot as plt

from pdfstream.transformation.main import get_pdf


def test_get_pdf(test_data):
    get_pdf(test_data['Ni_config'], test_data['Ni_chi'])
    plt.close()
