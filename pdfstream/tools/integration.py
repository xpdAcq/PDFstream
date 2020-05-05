"""The functions used in the integration pipelines. All functions consume namespace and return the modified
namespace. """
import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
from xpdtools.tools import generate_binner, mask_img

__all__ = ['bg_sub', 'auto_mask', 'integrate', 'visualize']

# default mask_img auto mask setting
_AUTOMASK_SETTING = dict(
    edge=30,
    lower_thresh=0.0,
    upper_thresh=None,
    alpha=2.0,
    auto_type='median',
    tmsk=None
)
# default pyfai integration setting
_INTEG_SETTING = dict(
    filename=None,
    npt=1480,
    correctSolidAngle=False,
    variance=None,
    error_model=None,
    radial_range=None,
    azimuth_range=None,
    dummy=None,
    delta_dummy=None,
    polarization_factor=0.99,
    dark=None,
    flat=None,
    method='splitpixel',
    unit='q_A^-1',
    safe=False,
    normalization_factor=1.0,
    block_size=32,
    profile=False,
    metadata=None
)
# default visualization setting
_PLOT_SETTING = {
    'figsize': (8, 4),
    'xlabel': {
        "q_A^-1": r"Q ($\mathrm{\AA}^{-1}$)",
        "q_nm^-1": r"Q ({nm}$^{-1}$)",
        "2th_deg": r"2$\theta$ (deg)",
        "2th_rad": r"2$\theta$ (rad)",
        "r_mm": r"radius (mm)",
    },
    'ylabel': 'I (A. U.)',
    'z_score': 2.
}


def bg_sub(img: ndarray, bg_img: ndarray, bg_scale: float = None):
    """Subtract the background image from the data image inplace.

    Parameters
    ----------
    img : ndarray
        The 2D diffraction image array.

    bg_img : ndarray
        The 2D background image array.

    bg_scale : float
        The scale of the the background image.
    """
    if bg_scale is None:
        bg_scale = 1.
    if bg_img.shape != img.shape:
        raise ValueError(f"Unmatched shape between bg_img and img: {bg_img.shape}, {img.shape}.")
    img = img - bg_scale * bg_img
    return img


def auto_mask(img: ndarray, ai: AzimuthalIntegrator, mask_setting: dict = None):
    """Automatically generate the mask of the image.

    Parameters
    ----------
    img : ndarray
        The 2D diffraction image array.

    ai : AzimuthalIntegrator
        The AzimuthalIntegrator instance.

    mask_setting : dict
        The user's modification to auto-masking settings.

    kwargs
        The other keywords not used in this function.

    Returns
    -------
    mask : ndarray
        The mask as a boolean array. True pixels are good pixels, False pixels are masked out.

    _mask_setting : dict
        The whole mask_setting.
    """
    _mask_setting = _AUTOMASK_SETTING.copy()
    if mask_setting is not None:
        _mask_setting.update(mask_setting)
    binner = generate_binner(ai, img.shape)
    mask = mask_img(img, binner, **_mask_setting)
    return mask, _mask_setting


def integrate(img: ndarray, ai: AzimuthalIntegrator, mask: ndarray = None, integ_setting: dict = None):
    """Use AzimuthalIntegrator to integrate the image. Add chi_x, chi_y, _integ_setting to namespace.

    Parameters
    ----------
    img : ndarray
        The 2D diffraction image array.

    ai : AzimuthalIntegrator
        The AzimuthalIntegrator instance.

    mask : ndarray
        The mask as a boolean array. True pixels are good pixels, False pixels are masked out.

    integ_setting : dict
        The user's modification to integration settings.

    Returns
    -------
    chi : ndarray
        The chi data. The first row is bin centers and the second row is the average intensity in bins.

    _integ_setting: dict
        The whole integration setting.
    """
    # merge integrate setting
    _integ_setting = _INTEG_SETTING.copy()
    _integ_setting.update(mask=mask)
    if integ_setting is not None:
        _integ_setting.update(integ_setting)
    del integ_setting
    # integrate
    chi = np.stack(
        ai.integrate1d(img, **_integ_setting)
    )
    return chi, _integ_setting


def visualize(img: ndarray, chi: ndarray, _integ_setting: dict, plot_setting: dict = None):
    """Visualize the processed image and the integrated curve.

    Parameters
    ----------
    img : ndarray
        The 2D diffraction image array.

    chi : ndarray
        The chi data. The first row is bin centers and the second row is the average intensity in bins.

    _integ_setting: dict
        The whole integration setting.

    plot_setting : dict
        The user's modification to integration settings.
    """
    _plot_setting = _PLOT_SETTING.copy()
    if plot_setting is not None:
        _plot_setting.update(plot_setting)
    plt.figure(figsize=_plot_setting['figsize'])
    plt.subplot(121)
    plt.plot(chi[0], chi[1])
    unit = _integ_setting['unit']
    plt.xlabel(_plot_setting['xlabel'][unit])
    plt.ylabel(_plot_setting['ylabel'])
    plt.subplot(122)
    mask = _integ_setting['mask']
    img = np.ma.masked_array(img, mask)
    mean, std = img.mean(), img.std()
    plt.imshow(
        img,
        vmin=mean - _plot_setting['z_score'] * std,
        vmax=mean + _plot_setting['z_score'] * std
    )
    plt.show(block=False)
    return
