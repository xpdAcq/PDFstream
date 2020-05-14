"""The command line intefrace function."""
from typing import Iterable, Union

import streamz as sz
from streamz import Stream

import pdfstream.pipelines as pl
import pdfstream.tools.io as io


def image_to_iq(img_files: Union[str, Iterable[str]], poni_file: str, bg_img_file: str = None, chi_file: str = None,
                bg_scale: float = None, mask_setting: dict = None,
                integ_setting: dict = None, plot_setting: dict = None, img_settings: dict = None):
    """"""
    if isinstance(img_files, str):
        img_files = (img_files,)
    # create input nodes
    _img_file = Stream()
    _img = sz.map(_img_file, io.load_img)
    _poni_file = Stream()
    _ai = sz.map(_poni_file, io.load_ai_from_poni_file)
    _bg_img_file = Stream()
    if bg_img_file is not None:
        _bg_img = sz.map(_img_file, io.load_img)
    else:
        _bg_img = None
    # build pipeline
    integ_setting.update({'filename': chi_file})
    pl.integration(_img, _ai, _bg_img, bg_scale=bg_scale, mask_setting=mask_setting, integ_setting=integ_setting,
                   plot_settings=plot_setting, img_settings=img_settings)
    # input data
    _poni_file.emit(poni_file)
    if bg_img_file is not None:
        _bg_img_file.emit(bg_img_file)
    for img_file in img_files:
        _img_file.emit(img_file)
    return


def iq_to_gr():
    return


def vis_fit():
    return


def vis_data():
    return
