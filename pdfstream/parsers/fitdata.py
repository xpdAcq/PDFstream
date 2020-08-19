import numpy as np

import pdfstream.parsers.tools as tools


def dict_to_array(dct: dict, keys: tuple, data_keys: tuple = ("x", "ycalc", "y"), **kwargs):
    """Convert a dictionary of str and list pairs to a numpy array.

    Parameters
    ----------
    dct : dict
        The dictionary that contains a sub-dictionary of str and list pairs.

    keys : tuple
        A key chain to find the sub-dictionary of str and list pairs.

    data_keys : tuple
        A dictionary of data keys. Their corresponding value will be added into the numpy array.

    kwargs : dict
        The kwargs for the `:func:~numpy.stack`.

    Returns
    -------
    array : ndarray
        The numpy array of data. Each row corresponding to a list in the dictionary.
    """
    data_dct = tools.get_value(dct, keys)
    return np.stack(
        (
            data_dct[key] for key in data_keys
        ),
        **kwargs
    )
