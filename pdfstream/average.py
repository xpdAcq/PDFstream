import typing as tp

import numpy as np
from numpy import ndarray


def main(imgs: tp.Iterable[ndarray], weights: tp.Iterable[float] = None) -> ndarray:
    """Average the 2D images.

    Parameters
    ----------
    imgs : ndarray
        The 2D array of diffraction images.

    weights : an iterable of floats
        The weights for the images. If None, images will not be weighted when averaged.

    Returns
    -------
    avg_img : ndarray
        The averaged 2D image array.
    """
    return np.average(np.stack(imgs, axis=0), weights=weights, axis=0)
