import typing as tp

import numpy as np
from matplotlib.axes import Axes

import pdfstream.parsers as parsers
from pdfstream.visualization.main import waterfall


def fitted_curves(docs: tp.Iterable[dict], keys: tuple = ('conresults', 0), data_keys: tuple = ("x", "ycalc", "y"),
                  rw_key: str = "rw", rw_template: str = r"$R_w$ = {:.2f}", **kwargs) -> Axes:
    """Visualize the fitted curves from the documents.

    Parameters
    ----------
    docs : Iterable[dict]
        A series of documentations.

    keys : tuple
        A key chain to find the sub-dictionary of str and list pairs.

    data_keys : tuple
        A dictionary of data keys. Their corresponding value will be added into the numpy array.

    rw_key : str
        The key of the value of goodness of fits.

    rw_template : str
        The template of how rw is show in the texts in the figure.

    kwargs : dict
        The kwargs for the `:func:~pdfstream.visualization.waterfall`.

    """
    data = parsers.dicts_to_array(docs, keys=keys, data_keys=data_keys)
    rws = parsers.dicts_to_array(docs, keys=keys, data_keys=(rw_key,))
    rws = np.squeeze(rws)
    texts = [rw_template.format(rw) for rw in rws]
    return waterfall(
        data, texts=texts, mode="fit", **kwargs
    )
