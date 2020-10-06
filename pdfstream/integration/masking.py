from typing import Tuple

import numpy as np
from numpy.core._multiarray_umath import ndarray
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator

from pdfstream.vend.masking import generate_binner, mask_img


def auto_mask(
    img: ndarray, ai: AzimuthalIntegrator, user_mask: ndarray = None, mask_setting: dict = None
) -> Tuple[ndarray, dict]:
    """Automatically generate the mask of the image.

    Parameters
    ----------
    img : ndarray
        The 2D diffraction image array.

    ai : AzimuthalIntegrator
        The AzimuthalIntegrator instance.

    mask_setting : dict
        The user's modification to auto-masking settings.

    user_mask : ndarray
        A mask provided by user. The auto generated mask will be multiplied by this mask.

    Returns
    -------
    mask : ndarray
        The mask as a boolean array. 0 are good pixels, 1 are masked out.

    _mask_setting : dict
        The whole mask_setting.
    """
    if mask_setting is not None:
        _mask_setting = mask_setting
    else:
        _mask_setting = dict()
    binner = generate_binner(ai, img.shape)
    tmsk = np.invert(user_mask.astype(bool)) if user_mask is not None else None
    mask = np.invert(mask_img(img, binner, tmsk=tmsk, **_mask_setting)).astype(int)
    return mask, _mask_setting
