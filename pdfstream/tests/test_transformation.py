from pdfstream.transformation.main import *


def test_get_pdf(db):
    get_pdf(db['Ni_config'], db['Ni_chi'])
    return
