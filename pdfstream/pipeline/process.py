import typing

from numpy import ndarray
from pyFAI import AzimuthalIntegrator

from pdfstream.integration import get_chi


def reduce(
    ai: AzimuthalIntegrator,
    img: ndarray,
    dk_img: ndarray,
    bg_img: ndarray,
    mask: ndarray = None,
    bg_scale: float = None,
    mask_setting: typing.Union[str, dict] = None,
    integ_setting: dict = None,
    **kwargs
) -> typing.Tuple[
    ndarray,
    dict,
    ndarray,
    typing.Union[None, ndarray],
    typing.Union[str, dict]
]:
    """A wrapper for the `~pdfstream.integration.get_chi`. See the function for details.

    The function is used in the pipeline. It assumes the ai, img, dk_img, bg_img come from the experiment or
    database. If user would like to apply them explicitly with their own data, add "user_" prefix at the front
    of the variable name, like "user_bg_img". The function will use the user data instead.
    """
    ai = kwargs.get("user_ai", ai)
    img = kwargs.get("user_img", img)
    dk_img = kwargs.get("user_dk_img", dk_img)
    bg_img = kwargs.get("user_bg_img", bg_img)
    return get_chi(
        ai, img, dk_img=dk_img, bg_img=bg_img, mask=mask, bg_scale=bg_scale, mask_setting=mask_setting,
        integ_setting=integ_setting, img_setting="OFF", plot_setting="OFF"
    )
