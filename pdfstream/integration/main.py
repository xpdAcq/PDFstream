import typing as tp

import numpy as np
from numpy import ndarray
from pyFAI import AzimuthalIntegrator

from pdfstream.integration.tools import bg_sub, vis_img, integrate, vis_chi, auto_mask


def get_chi(
    ai: AzimuthalIntegrator,
    img: ndarray,
    dk_img: ndarray = None,
    bg_img: ndarray = None,
    mask: ndarray = None,
    bg_scale: float = None,
    mask_setting: tp.Union[str, dict] = None,
    integ_setting: dict = None,
    img_setting: tp.Union[str, dict] = None,
    plot_setting: tp.Union[str, dict] = None,
) -> tp.Tuple[
    ndarray,
    ndarray,
    ndarray,
    ndarray,
    tp.Union[None, ndarray],
    dict,
    tp.Union[str, dict]
]:
    """Process the diffraction image to get I(Q).

    The image will be subtracted by the background image and then auto masked. The results will be
    binned on the azimuthal direction and the average value of the intensity in the bin and their
    corresponding Q will be returned. The I(Q) and background subtracted masked image will
    be visualized.

    Parameters
    ----------
    ai : AzimuthalIntegrator
        The AzimuthalIntegrator.

    img : ndarray
        The of the 2D array of the image.

    dk_img : ndarray
        The dark frame image. The image will be subtracted by it if provided.

    bg_img : ndarray
        The 2D array of the background image. If None, no background subtraction.

    mask : ndarray
        A mask provided by user. The auto generated mask will be multiplied by this mask.

    bg_scale : float
        The scale for background subtraction. If None, use 1.

    mask_setting : dict
        The auto final_mask setting.
        If None, use _AUTOMASK_SETTING in the tools module. To turn off the auto masking, use "OFF".

    integ_setting : dict
        The integration setting.
        If None, use _INTEG_SETTING in the tools module.

    img_setting : dict
        The user's modification to imshow kwargs except a special key 'z_score'. If None, use use empty dict.
        To turn off the imshow, use "OFF".

    plot_setting : dict
        The kwargs for the plot function. If None, use empty dict.

    Returns
    -------
    chi : ndarray
        The 2D array of integrated results. The first row is the Q and the second row is the I.

    bg_sub_img : ndarray
        The background subtracted image. If no background subtraction, it is the dk_sub_image.

    dk_sub_img : ndarray
        The dark subtracted image. If no dark subtraction, it is the input img.

    img : ndarray
        The input image.

    final_mask : ndarray or None
        The final_mask array. If no auto_masking, return None.

    _integ_setting: dict
        The integration setting used.

    _mask_setting : dict or str
        The auto masking setting.
    """
    if dk_img is not None:
        dk_sub_img = bg_sub(img, dk_img, bg_scale=1.)
    else:
        dk_sub_img = img
    if bg_img is not None:
        bg_sub_img = bg_sub(dk_sub_img, bg_img, bg_scale=bg_scale)
    else:
        bg_sub_img = dk_sub_img
    if mask_setting != "OFF":
        final_mask, _mask_setting = auto_mask(bg_sub_img, ai, user_mask=mask, mask_setting=mask_setting)
    elif mask is not None:
        final_mask, _mask_setting = mask, {}
    else:
        final_mask, _mask_setting = None, None
    if img_setting != "OFF":
        vis_img(bg_sub_img, final_mask, img_setting=img_setting)
    chi, _integ_setting = integrate(bg_sub_img, ai, mask=final_mask, integ_setting=integ_setting)
    if plot_setting != "OFF":
        vis_chi(chi, plot_setting=plot_setting, unit=_integ_setting.get('unit'))
    return chi, bg_sub_img, dk_sub_img, img, final_mask, _integ_setting, _mask_setting


def avg_imgs(imgs: tp.Iterable[ndarray], weights: tp.Iterable[float] = None) -> ndarray:
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
    return np.average(np.stack(tuple(imgs), axis=0), axis=0, weights=weights)
