"""Function interface that can be used in jupyter notebook. Pipelines will be built inside the function and data input will be processed to the pipeline."""
from typing import Iterable, Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from numpy import ndarray
from streamz import Stream

import pdfstream.pipelines as pipelines
import pdfstream.tools.visualization as vis


def init_pipe(pipe: Callable, text: str = None, **kwargs):
    """"""
    _data = Stream()
    _ax = Stream()
    _text = Stream() if text is not None else None
    pipe(_data, _ax, _text, **kwargs)
    return _ax, _data, _text


def vis_waterfall(dataset: Iterable[ndarray], texts: Iterable[str] = None, ax: Axes = None, **kwargs):
    """"""
    if ax is None:
        ax = plt.gca()
    _data, _ax, _text = init_pipe(pipelines.vis_waterfall, texts, **kwargs)
    _ax.emit(ax)
    if _text is None:
        for data in dataset:
            _data.emit(data)
    else:
        for data, text in zip(dataset, texts):
            _data.emit(data)
            _text.emit(text)
    return


def vis_fit_waterfall(dataset: Iterable[ndarray], texts: Iterable[str] = None, ax: Axes = None, **kwargs):
    """"""
    if ax is None:
        ax = plt.gca()
    _data, _ax, _text = init_pipe(pipelines.vis_fit_waterfall, texts, **kwargs)
    _ax.emit(ax)
    if _text is None:
        for data in dataset:
            _data.emit(data)
    else:
        for data, text in zip(dataset, texts):
            _data.emit(data)
            _text.emit(text)
    return


def vis_dff(data0: ndarray, data1: ndarray, text: str = None, ax: Axes = None, **kwargs):
    """"""
    if not np.array_equal(data0[0], data1[1]):
        raise ValueError('The first rows of data0 and data1 are not equal. Two data is not on the same grid.')
    if kwargs.pop('normalize', False):
        data0 = vis.normalize(data0)
        data1 = vis.normalize(data1)
    data = np.stack((data0[1], data1[1], data1[1] - data0[1]))
    kwargs.update({'normalize': False, 'shift': False})
    vis_fit_waterfall([data], text, ax, **kwargs)
    return
