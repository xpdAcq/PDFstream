"""The command line intefrace function."""
from pathlib import Path
from typing import Iterable, Union

import streamz as sz
from streamz import Stream

import pdfstream.pipelines as pl
import pdfstream.tools.io as io


def integrate(img_files: Union[str, Iterable[str]],
              poni_file: str,
              bg_img_file: str = None,
              output_dir: str = ".",
              bg_scale: float = None,
              mask_setting: Union[dict, str] = None,
              integ_setting: dict = None,
              plot_setting: Union[dict, str] = None,
              img_settings: Union[dict, str] = None):
    """Azimuthal integration of the two dimensional diffraction image.

    The image will be first subtracted by background if background image file is given. Then, it will be binned
    in azimuthal direction according to the geometry provided by the poni file. The pixels far away from the
    average in each bin will be masked. The mask will be applied on the background subtracted image and the
    image will be integrated again by the pyFAI. The polarization correction and pixel-splitting algorithm will
    be applied according to user settings before the integration. The results are saved as chi files.

    Examples
    --------
    image_to_iq diffraction_image.tiff calibrant.poni --bg_img_file background.tiff --integ_setting {npt: 2048}

    Parameters
    ----------
    img_files : str or iterable of str
        The path to the image file. It will be read by fabio.

    poni_file : str
        The path to the poni file. It will be read by pyFAI.

    bg_img_file : str
        The path to the background image file. It should have the same dimension as the data image. If None,
        no background subtraction will be done.

    output_dir : str
        The directory to save the image file. Default current working directory.

    bg_scale : float
        The scale of the background. Default 1

    mask_setting : dict
        The settings for the auto-masking. See the arguments for mask_img (
        https://xpdacq.github.io/xpdtools/xpdtools.html?highlight=mask_img#xpdtools.tools.mask_img). To turn
        off the auto masking, enter "OFF".

    integ_setting : dict
        The settings for the integration. See the arguments for integrate1d (
        https://pyfai.readthedocs.io/en/latest/api/pyFAI.html#module-pyFAI.azimuthalIntegrator).

    plot_setting : dict
        The keywords for the matplotlib.pyplot.plot (
        https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.plot.html). To turn off the plotting,
        enter "OFF".

    img_settings : dict
        The keywords for the matplotlib.pyplot.imshow (
        https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.imshow.html). Besides, there is a key
        'z_score', which determines the range of the colormap. The range is mean +/- z_score * std in the
        statistics of the image. To turn of the image, enter "OFF".
    """
    if integ_setting is None:
        integ_setting = dict()
    if plot_setting is None:
        plot_setting = dict()
    if img_settings is None:
        img_settings = dict()
    if isinstance(img_files, str):
        img_files = (img_files,)
    # input nodes
    _img_file = Stream()
    _img = sz.map(_img_file, io.load_img)
    _poni_file = Stream()
    _ai = sz.map(_poni_file, io.load_ai_from_poni_file)
    _bg_img_file = Stream()
    _bg_img = sz.map(_bg_img_file, lambda f: io.load_img(f) if f is not None else None)
    # build pipeline
    _chi, _, _ = pl.integration(_img, _ai, _bg_img, bg_scale=bg_scale,
                                mask_setting=mask_setting,
                                integ_settings=integ_setting,
                                plot_settings=plot_setting, img_settings=img_settings)
    # get the node to change filename settings
    integ_node = _chi.upstream
    # input data
    for img_file in img_files:
        # the output file name is the image file name with .chi extension
        chi_file = Path(output_dir).joinpath(Path(img_file).with_suffix(".chi").name)
        # update the integration setting to output different files
        integ_node.kwargs['integ_settings'].update({"filename": str(chi_file)})
        _poni_file.emit(poni_file)
        _bg_img_file.emit(bg_img_file)
        _img_file.emit(img_file)
    return


def iq_to_gr():
    return


def vis_fit():
    return


def vis_data():
    return
