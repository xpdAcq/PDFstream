from pprint import pprint

import matplotlib.pyplot as plt
import streamz as sz
from tests import *

import pdfstream.pipelines as pipelines
import pdfstream.tools.io as io


def test_integration():
    img, ai, bg_img = sz.Stream(), sz.Stream(), sz.Stream()
    result = sz.combine_latest(*pipelines.integration(img, ai, bg_img))
    sz.sink(result, pprint)
    img.emit(NI_IMG)
    ai.emit(io.load_ai_from_poni_file('data/Ni_calib.poni'))
    bg_img.emit(BG_IMG)


def test_get_pdf():
    chi = sz.Stream()
    pdfconfig = sz.Stream()
    pdfgetter = pipelines.get_pdf(chi, pdfconfig)
    pdfgetter.sink(pprint)
    chi.emit(NI_CHI)
    pdfconfig.emit(io.load_pdfconfig('data/Ni.gr'))


def test_vis_waterfall():
    data = sz.Stream()
    text = sz.Stream()
    ax = sz.Stream()
    fig = plt.figure()
    _ax = fig.add_subplot(111)
    res = pipelines.vis_waterfall(data, ax, text, label_type='gr')
    sz.sink(res, pprint)
    ax.emit(_ax)
    data.emit(NI_GR)
    text.emit('Ni')
    data.emit(NI_GR)
    text.emit('Ni')
    fig.savefig('local/waterfall.png')


def test_vis_fit():
    data = sz.Stream()
    ax = sz.Stream()
    text = sz.Stream()
    fig = plt.figure()
    _ax = fig.add_subplot(111)
    res = pipelines.vis_fit_waterfall(data, ax, text, label_type='fgr')
    sz.sink(res, pprint)
    ax.emit(_ax)
    data.emit(NI_FGR)
    text.emit('Ni')
    data.emit(NI_FGR)
    text.emit('Ni')
    fig.savefig('local/fit.png')
