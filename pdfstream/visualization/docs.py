import itertools
import typing as tp

import numpy as np
from matplotlib.axes import Axes

import pdfstream.parsers as parsers
from pdfstream.visualization.main import waterfall


def fitted_curves(docs: tp.Iterable[dict], text_keys: tuple = None, keys: tuple = ('conresults', 0),
                  data_keys: tuple = ("x", "y", "ycalc"), rw_key: str = "rw",
                  rw_template: str = r"$R_w$ = {"r":.2f}",
                  text_template: str = r"{}",
                  **kwargs) -> Axes:
    """Visualize the fitted curves from the documents.

    Parameters
    ----------
    docs : Iterable[dict]
        A series of documentations.

    text_keys : Iterable[str]
        The text to annotate the curves.

    keys : tuple
        A key chain to find the sub-dictionary of str and list pairs.

    data_keys : tuple
        A dictionary of data keys. Their corresponding value will be added into the numpy array.

    rw_key : str
        The key of the value of goodness of fits.

    rw_template : str
        The template of how rw is show in the texts in the figure.

    text_template : str
        The template of how text is how in the figure.

    kwargs : dict
        The kwargs for the `:func:~pdfstream.visualization.waterfall`.

    """
    data = parsers.dicts_to_array(docs, keys=keys, data_keys=data_keys)
    rws = parsers.dicts_to_array(docs, keys=keys, data_keys=(rw_key,))
    texts = [rw_template.format(rw) for rw in rws[:, 0]]
    if text_keys:
        raw_texts = parsers.dicts_to_array(docs, keys=text_keys[:-1], data_keys=(text_keys[-1],))
        raw_texts = np.squeeze(raw_texts)
        raw_texts = [text_template.format(raw_text) for raw_text in raw_texts]
        texts = [
            '{}\n{}'.format(raw_text, text)
            for raw_text, text in itertools.zip_longest(raw_texts, texts)
        ]
    return waterfall(
        data, texts=texts, mode="fit", **kwargs
    )
