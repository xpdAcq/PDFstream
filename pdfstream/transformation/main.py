import typing

from diffpy.pdfgetx import PDFConfig, PDFGetter
from numpy import ndarray

from pdfstream.transformation.tools import make_pdfgetter, use_pdfgetter, visualize

__all__ = [
    'get_pdf'
]


def get_pdf(pdfconfig: PDFConfig, chi: ndarray, plot_setting: typing.Union[str, dict] = None) -> PDFGetter:
    """Get the PDF from the chi data.

    The pdfgetter will be initiated by pdfconfig. It takes the chi data and does the calculation. The results
    will be visualized.

    Parameters
    ----------
    pdfconfig : PDFConfig
        This class stores all configuration data needed for generating PDF. See diffpy.pdfgetx.PDFConfig.

    chi : ndarray
        The array of chi data. The first row is Q or two theta, the second row is intensity.

    plot_setting : dict or 'OFF'
        The kwargs of plotting. See matplotlib.pyplot.plot. If 'OFF', skip visualization.

    test : bool
        If True, run in test mode.

    Returns
    -------
    pdfgetter :
        The PDFGetter.
    """
    pdfgetter = make_pdfgetter(pdfconfig)
    use_pdfgetter(chi, pdfgetter)
    if plot_setting != "OFF":
        visualize(pdfgetter, plot_setting)
    return pdfgetter
