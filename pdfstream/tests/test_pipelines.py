from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import streamz as sz
from diffpy.pdfgetx import PDFGetter

import pdfstream.pipelines as pipelines


def test_integration(db):
    img, ai, bg_img = sz.Stream(), sz.Stream(), sz.Stream()
    img1, _integ_setting, _mask_setting = pipelines.integration(
        img, ai, bg_img, plot_settings=pipelines.OFF, img_settings=pipelines.OFF
    )
    lst0 = img1.sink_to_list()
    lst1 = _integ_setting.sink_to_list()
    lst2 = _mask_setting.sink_to_list()
    img.emit(db.get('black_img'))
    ai.emit(db.get('ai'))
    bg_img.emit(db.get('black_img'))
    assert isinstance(lst0.pop(), np.ndarray)  # img are zeros so it will be the same after the pipeline
    assert isinstance(lst1.pop(), dict)  # integration settings
    assert isinstance(lst2.pop(), dict)  # auto-masking settings


def test_get_pdf(db):
    chi = sz.Stream()
    pdfconfig = sz.Stream()
    pdfgetter = pipelines.get_pdf(chi, pdfconfig)
    lst = pdfgetter.sink_to_list()
    pdfgetter.sink(pprint)
    chi.emit(db.get('Ni_chi'))
    pdfconfig.emit(db.get('Ni_config'))
    assert isinstance(lst.pop(), PDFGetter)


def test_vis_waterfall(db):
    data = sz.Stream()
    text = sz.Stream()
    ax = sz.Stream()
    fig = plt.figure()
    _ax = fig.add_subplot(111)
    res = pipelines.vis_waterfall(data, ax, text, label_type='gr')
    lst = res.sink_to_list()
    ax.emit(_ax)
    data.emit(db.get('Ni_gr'))
    text.emit('Ni')
    data.emit(db.get('Ni_gr'))
    text.emit('Ni')
    assert len(lst.pop().lines) == 2


def test_vis_fit_waterfall(db):
    data = sz.Stream()
    ax = sz.Stream()
    text = sz.Stream()
    fig = plt.figure()
    _ax = fig.add_subplot(111)
    res = pipelines.vis_fit_waterfall(data, ax, text, label_type='fgr')
    lst = res.sink_to_list()
    ax.emit(_ax)
    data.emit(db.get('Ni_fgr'))
    text.emit('Ni')
    data.emit(db.get('Ni_fgr'))
    text.emit('Ni')
    assert len(lst.pop().lines) == 8
