import typing as tp

from numpy import ndarray

from pdfstream.integration.main import get_chi, AzimuthalIntegrator
from pdfstream.modeling.main import fit_calib, Crystal, MyParser, FIT_RANGE, MyRecipe
from pdfstream.transformation.main import get_pdf, PDFConfig, PDFGetter

__all__ = [
    'calib_pipe'
]


def calib_pipe(
        ai: AzimuthalIntegrator, pdfconfig: PDFConfig, stru: Crystal, img: ndarray, fit_range: FIT_RANGE,
        qdamp0: float = 0.04, qbroad0: float = 0.02, bg_img: ndarray = None, bg_scale: float = None,
        mask_setting: dict = None, integ_setting: dict = None, img_setting: dict = None, chi_plot_setting: dict
        = None, pdf_plot_setting: dict = None, ncpu: int = None
) -> tp.Tuple[PDFGetter, MyRecipe]:
    """ Pipeline-style qdamp, qbroad calibration.

    A pipeline to do image background subtraction, auto masking, integration, PDF transformation and PDF
    modeling to calibrate the qdamp and qbroad. Also, the accuracy of the calibration is tested by the modeling.

    Parameters
    ----------
    ai : AzimuthalIntegrator
        The AzimuthalIntegrator.

    pdfconfig : PDFConfig
        This class stores all configuration data needed for generating PDF. See diffpy.pdfgetx.PDFConfig.

    stru : Crystal
        The structure of calibration material.

    img : ndarray
        The of the 2D array of the image.

    fit_range : tuple
        The rmin, rmax and rstep in the unit of angstrom.

    bg_img : ndarray
        The 2D array of the background image. If None, no background subtraction.

    bg_scale : float
        The scale for background subtraction. If None, use 1.

    mask_setting : dict
        The auto mask setting. See _AUTO_MASK_SETTING in pdfstream.tools.integration. If None,
        use _AUTOMASK_SETTING. To turn off the auto masking, use "OFF".

    integ_setting : dict
        The integration setting. See _INTEG_SETTING in pdfstream.tools.integration. If None, use _INTEG_SETTING.

    img_setting : dict
        The user's modification to imshow kwargs except a special key 'z_score'. If None, use use empty dict.
        To turn off the imshow, use "OFF".

    chi_plot_setting : dict
        The kwargs of chi data plotting. See matplotlib.pyplot.plot. If 'OFF', skip visualization.

    pdf_plot_setting : dict or 'OFF'
        The kwargs of pdf data plotting. See matplotlib.pyplot.plot. If 'OFF', skip visualization.

    ncpu : int
        The number of cpu used in parallel computing. If None, no parallel computing.

    Returns
    -------
    pdfgetter : PDFGetter
        The object with processed data, including iq, sq, fq, gr.

    recipe : MyRecipe
        The refined recipe of the fitting.
    """
    chi = get_chi(
        ai, img, bg_img=bg_img, bg_scale=bg_scale, mask_setting=mask_setting, integ_setting=integ_setting,
        img_setting=img_setting, plot_setting=chi_plot_setting
    )
    pdfgetter = get_pdf(pdfconfig, chi, plot_setting=pdf_plot_setting)
    data = MyParser()
    data.parsePDFGetter(pdfgetter, add_meta={'qdamp': qdamp0, 'qbroad': qbroad0})
    recipe = fit_calib(stru, data, fit_range, ncpu=ncpu)
    return pdfgetter, recipe
