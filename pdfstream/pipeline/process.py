"""Process the information."""
import numpy
import typing
from diffpy.pdfgetx import PDFConfig, PDFGetter
from numpy import ndarray
from pyFAI import AzimuthalIntegrator
from xarray import DataArray

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
) -> typing.Tuple[DataArray, DataArray, DataArray, DataArray, DataArray]:
    """Process the image to PDF. Used in pipeline."""
    chi, _integ_setting, img, final_mask, _ = reduce(
        img=img, ai=ai, dk_img=dk_img, bg_img=bg_img, mask=mask, bg_scale=bg_scale, mask_setting=mask_setting,
        integ_setting=integ_setting, **kwargs
    )
    image = DataArray(
        numpy.ma.masked_array(img, mask=final_mask),
        name="image"
    )
    dataformat = get_dataformat(_integ_setting)
    if dataformat:
        config.update({"dataformat": dataformat})
    pdfgetter = transform(chi=chi, config=config, **kwargs)
    iq = DataArray(
        pdfgetter.iq[1],
        coords={"Q": pdfgetter.iq[0]},
        dims=["Q"],
        name="I"
    )
    sq = DataArray(
        pdfgetter.sq[1],
        coords={"Q": pdfgetter.sq[0]},
        dims=["Q"],
        name="S"
    )
    fq = DataArray(
        pdfgetter.sq[1],
        coords={"Q": pdfgetter.fq[0]},
        dims=["Q"],
        name="F"
    )
    gr = DataArray(
        pdfgetter.gr[1],
        coords={"r": pdfgetter.gr[0]},
        dims=["r"],
        name="G"
    )
    return image, iq, sq, fq, gr


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
    config = kwargs.get("user_config", config)
    _config.update(config)
    pdfconfig = PDFConfig(**_config)
    return get_pdf(pdfconfig, chi, plot_setting="OFF")
