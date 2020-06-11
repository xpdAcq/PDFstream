"""API to use pdfgetter to transform xrd data to pdf."""
from collections import OrderedDict

import matplotlib.pyplot as plt
from diffpy.pdfgetx import PDFGetter, PDFConfig
from matplotlib.gridspec import GridSpec
from numpy import ndarray


def make_pdfgetter(pdfconfig: PDFConfig, user_config: dict = None) -> PDFGetter:
    """Make the pdfgetter."""
    if user_config is not None:
        pdfconfig.update(**user_config)
    pdfgetter = PDFGetter(pdfconfig)
    return pdfgetter


def use_pdfgetter(chi: ndarray, pdfgetter: PDFGetter) -> PDFGetter:
    """Transform the data using the pdfgetter."""
    if len(chi.shape) != 2:
        raise ValueError("Wrong data shape in chi: {}".format(chi.shape))
    if chi.shape[0] != 2:
        raise ValueError("Wrong number of rows in chi: {}".format(chi.shape[0]))
    pdfgetter(chi[0], chi[1])
    return pdfgetter


def visualize(pdfgetter: PDFGetter):
    """Visualize data in pdfgetter."""
    # get data
    dct = OrderedDict()
    for attr in ("iq", "sq", "fq", "gr"):
        tup = getattr(pdfgetter, attr)
        if len(tup) > 0:
            dct[attr] = tup
    # plot data
    fig = plt.figure(figsize=(6, 6 * len(dct)))
    grids = GridSpec(len(dct), 1)
    labels = {
        "iq": (r"Q ($\AA^{-1}$)", r"I (A. U.)"),
        "sq": (r"Q ($\AA^{-1}$)", r"S"),
        "fq": (r"Q ($\AA^{-1}$)", r"F ($\AA^{-1}$)"),
        "gr": (r"r ($\AA$)", r"G ($\AA^{-2}$)")
    }
    for grid, (dtype, tup) in zip(grids, dct.items()):
        x, y = tup
        xlabel, ylabel = labels.get(dtype)
        ax = fig.add_subplot(grid)
        ax.plot_line(x, y)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    return
