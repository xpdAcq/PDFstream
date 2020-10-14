"""Process the information."""
import numpy
import typing
from diffpy.pdfgetx import PDFConfig, PDFGetter
from numpy import ndarray
from pyFAI import AzimuthalIntegrator

from pdfstream.integration import get_chi
from pdfstream.transformation import get_pdf

_DATAFORMAT = {
    "q_nm^-1": "Qnm",
    "q_A^-1": "QA",
    "2th_deg": "twotheta"
}
_DEFAULT_CONFIG = {
    "dataformat": "QA",
    "outputtypes": []
}
DATA = typing.Dict[str, ndarray]


def process_img_to_pdf(
    img: ndarray,
    ai: AzimuthalIntegrator,
    dk_img: typing.Union[None, ndarray],
    bg_img: typing.Union[None, ndarray],
    config: dict,
    mask: ndarray = None,
    bg_scale: float = None,
    mask_setting: typing.Union[str, dict] = None,
    integ_setting: dict = None,
    **kwargs
) -> typing.Tuple[DATA, DATA, DATA, DATA, DATA, DATA]:
    """Process the image to PDF. Used in pipeline."""
    _chi, _integ_setting, img, final_mask, _ = reduce(
        img=img, ai=ai, dk_img=dk_img, bg_img=bg_img, mask=mask, bg_scale=bg_scale, mask_setting=mask_setting,
        integ_setting=integ_setting, **kwargs
    )
    dataformat = get_dataformat(_integ_setting)
    if dataformat:
        config.update({"dataformat": dataformat})
    pdfgetter = transform(chi=_chi, config=config, **kwargs)
    image = {"image": img}
    masked_img = {"masked_image": numpy.ma.masked_array(img, final_mask)}
    iq = {"Q": pdfgetter.iq[0], "I": pdfgetter.iq[1]}
    sq = {"Q": pdfgetter.sq[0], "S": pdfgetter.sq[1]}
    fq = {"Q": pdfgetter.fq[0], "F": pdfgetter.fq[1]}
    gr = {"r": pdfgetter.gr[0], "G": pdfgetter.gr[1]}
    return image, masked_img, iq, sq, fq, gr


def get_dataformat(_integ_setting: dict) -> typing.Union[None, str]:
    if "unit" in _integ_setting:
        unit = _integ_setting["unit"]
        if unit in _DATAFORMAT:
            return _DATAFORMAT[unit]
        else:
            allowed = ",".join(_DATAFORMAT.keys())
            raise ValueError(
                "Cannot transfer data with unit {}. Expect {}.".format(unit, allowed)
            )
    return None


def reduce(
    img: ndarray,
    ai: AzimuthalIntegrator,
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
    """A wrapper for the `~pdfstream.integration.get_chi`. See the function for details."""
    dk_img = kwargs.get("user_dk_img", dk_img)
    bg_img = kwargs.get("user_bg_img", bg_img)
    ai = kwargs.get("user_ai", ai)
    return get_chi(
        ai, img, dk_img=dk_img, bg_img=bg_img, mask=mask, bg_scale=bg_scale, mask_setting=mask_setting,
        integ_setting=integ_setting, img_setting="OFF", plot_setting="OFF"
    )


def transform(
    chi: ndarray,
    config: dict,
    **kwargs
) -> PDFGetter:
    """A wrapper for the `~pdfstream.transformation.get_pdf`. See the function for details."""
    _config = _DEFAULT_CONFIG.copy()
    if "user_config" in kwargs:
        config = kwargs["user_config"]
    _config.update(config)
    pdfconfig = PDFConfig(**_config)
    return get_pdf(pdfconfig, chi, plot_setting="OFF")
