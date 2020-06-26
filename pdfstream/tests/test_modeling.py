import matplotlib.pyplot as plt

from pdfstream.modeling.main import *


def test_MyParser(db):
    parser = MyParser()
    meta = {'qmin': 1, 'qmax': 24, 'qdamp': 0.04, 'qbroad': 0.02}
    parser.parseDict(db['Ni_gr'], meta=meta)
    recipe = multi_phase([db['Ni_stru']], parser, fit_range=(0., 8., .1))
    gen = recipe.multi_phase.G0
    assert gen.getQmin() == meta['qmin']
    assert gen.getQmax() == meta['qmax']
    assert gen.qdamp.value == meta['qdamp']
    assert gen.qbroad.value == meta['qbroad']


def test_fit_calib(db):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    fit_calib(db['Ni_stru'], parser, fit_range=(2., 8., .1))
    plt.close()
