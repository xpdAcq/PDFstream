"""The pipeline factory. All pipelines made by factories take in data from streams. The processing configuration is tuned by other non-stream arguments."""

from typing import Tuple, Callable

import streamz as sz
from streamz import Stream

import pdfstream.integration.tools as integ
import pdfstream.transformation.tools as trans
import pdfstream.visualization.tools as vis


def integration(img: Stream, ai: Stream, bg_img: Stream, bg_scale: float = None,
                mask_setting: dict = None, integ_settings: dict = None, img_settings: dict = None, plot_settings:
        dict = None) -> Tuple[Stream, Stream, Stream]:
    """Make integration pipeline.

    Parameters
    ----------
    img : Stream
        A stream of the 2D ndarray of the image.

    ai : Stream
        A stream of the AzimuthalIntegrator.

    bg_img : Stream
        A stream of the 2D ndarray of the background image. If None, no background subtraction.

    bg_scale : float
        The scale for background subtraction.

    mask_setting : dict
        The auto mask setting. See _AUTO_MASK_SETTING in pdfstream.tools.integration. If None, use default.

    integ_settings : dict
        The integration setting. See _INTEG_SETTING in pdfstream.tools.integration. If None, use default.

    img_settings : dict
        The user's modification to imshow kwargs except a special key 'z_score'.

    plot_settings : dict
        The kwargs for the plot function.

    Returns
    -------
    chi : Stream
        The stream of 2D ndarray of chi data.

    _integ_setting : Stream
        The stream of whole integration setting.

    _mask_setting : Stream
        The stream of whole auto masking setting.
    """
    auto_mask_output = sz.starmap(sz.zip(img, ai), integ.auto_mask, mask_setting=mask_setting)
    mask = sz.pluck(auto_mask_output, 0, stream_name='mask')
    ax0 = sz.starmap(sz.zip(img, mask), integ.vis_img, img_settings=img_settings)
    sz.sink(ax0, lambda ax: None, stream_name="End")
    _mask_setting = sz.pluck(auto_mask_output, 1, stream_name='_mask_setting')
    img = sz.starmap(sz.zip(img, bg_img), integ.bg_sub, bg_scale)
    integrate_output = sz.starmap(sz.zip(img, ai, mask), integ.integrate, integ_settings=integ_settings)
    chi = sz.pluck(integrate_output, 0, stream_name='chi')
    _integ_setting = sz.pluck(integrate_output, 1, stream_name='_integ_setting')
    ax1 = sz.starmap(sz.zip(chi, _integ_setting), integ.vis_chi, plot_settings=plot_settings)
    sz.sink(ax1, lambda ax: None, stream_name="End")
    return chi, _integ_setting, _mask_setting


def get_pdf(chi: Stream, pdfconfig: Stream, user_config: dict = None) -> Stream:
    """Make the pipeline to transform the chi data to pdf data.

    Parameters
    ----------
    chi : Stream
        A stream of 2D ndarray of chi data.

    pdfconfig : Stream
        A stream of PDFConfig.

    user_config : dict
        User configuration to update the PDFConfig.

    Returns
    -------
    pdfgetter : Stream
        A stream of the pdfgetter that contains the data.
    """
    pdfgetter = sz.map(pdfconfig, trans.make_pdfgetter, user_config)
    pdfgetter = sz.starmap(sz.combine_latest(chi, pdfgetter), trans.use_pdfgetter)
    sz.sink(pdfgetter, trans.visualize)
    return pdfgetter


def _vis_waterfall(func: Callable, data: Stream, ax: Stream, text: Stream = None, label_type: str = None,
                   normalize: bool = True, shift: bool = True, line_spacing: float = None,
                   text_xy: Tuple[float, float] = None, line_ind: int = -1, **kwargs):
    """
    Apply a visualization for data stream and plot them in one axis in a waterfall.

    Parameters
    ----------
    func : Callable
        The visualization function f(data, ax, **kwargs).

    data : Stream
        A stream of data.

    ax : Stream
         A stream of Axes to plot data on.

    text : Stream
        A stream of string label.

    label_type :

    label_type : str
        The type of the auto label for axes.

    normalize : bool
        Whether to normalize the data by (max - min).

    shift : bool
        Whether to shift the data down.

    line_spacing : float
        The spacing of the max of current curve and the min of last curve.

    plot_setting : dict
        The kwargs for plot.

    text_xy : Tuple[float, float]
        The coordinates of the text relative to the horizontal axis and the max and local max of the data.

    line_ind : int
        The which line to annotate the text.

    kwargs : dict
        The kwargs for the func.

    Returns
    -------
    ax : Stream
        The stream of output ax.
    """
    ax = sz.map(ax, vis.set_minor_tick)
    if label_type is not None:
        ax = sz.map(ax, vis.auto_label, label_type)
    if normalize:
        data = sz.map(data, vis.normalize)
    if shift:
        data = sz.starmap(sz.combine_latest(data, ax), vis.shift, line_spacing=line_spacing)
    ax = sz.starmap(sz.combine_latest(data, ax), func, **kwargs)
    if text is not None:
        ax = sz.starmap(sz.zip(text, ax), vis.auto_text, text_xy=text_xy, line_ind=line_ind)
    return ax


def vis_waterfall(data: Stream, ax: Stream, text: Stream = None, label_type: str = None, normalize: bool = True,
                  shift: bool = True, line_spacing: float = None, plot_setting: dict = None,
                  text_xy: Tuple[float, float] = None) -> Stream:
    """
    Visualize xy data in a water fall plot. New data curve will be added below the last data curve.

    Parameters
    ----------
    data : Stream
        A stream of 2D ndarray data. First row is x and the second row is y.

    ax : Stream
        A stream of Axes to plot data on.

    text : Stream
        A stream of string label.

    label_type : str
        The type of the auto label for axes.

    normalize : bool
        Whether to normalize the data by (max - min).

    shift : bool
        Whether to shift the data down.

    line_spacing : float
        The spacing of the max of current curve and the min of last curve.

    plot_setting : dict
        The kwargs for plot.

    text_xy : Tuple[float, float]
        The coordinates of the text relative to the horizontal axis and the max and local max of the data.

    Returns
    -------
    ax : Stream
        A stream of Axes where data is plotted.
    """
    return _vis_waterfall(
        vis.plot, data, ax, text, label_type, normalize, shift, line_spacing,
        plot_setting=plot_setting, text_xy=text_xy, line_ind=-1
    )


def vis_fit_waterfall(data: Stream, ax: Stream, text: Stream = None, *, label_type: str = None,
                      normalize: bool = True,
                      shift: bool = True, line_spacing: float = None, xy_kwargs: dict = None,
                      xycalc_kwargs: dict = None,
                      xydiff_kwargs: dict = None, xyzero_kwargs: dict = None, fill_kwargs: dict = None,
                      text_xy: Tuple[float, float] = None) -> Stream:
    """
    Visualize fitted data in a single plot. The fit will be overlaid with the data and difference
    curve will be below the data with zero value line and fill in color.

    Parameters
    ----------
    data : Stream
        A stream of 2D ndarray data. First row is x and the second row is y.

    ax : Stream
        A stream of Axes to plot data on.

    text : Stream
        A stream of string label.

    label_type : str
        The type of the auto label for axes.

    normalize : bool
        Whether to normalize the data by (max - min).

    shift : bool
        Whether to shift the data down.

    line_spacing : float
        The spacing of the max of current curve and the min of last curve.

    xy_kwargs : dict
        The kwargs for the plot of data.

    xycalc_kwargs : dict
        The kwargs for the plot of the calculation.

    xydiff_kwargs : dict
        The kwargs for the plot of the difference curve.

    xyzero_kwargs : dict
        The kwargs for the plot of the zero line.

    fill_kwargs : dict
        The kwargs for the filling in color.

    text_xy : dict
        The position of the text relative to the data.

    Returns
    -------
    ax : Stream
        A stream of Axes where data is plotted.
    """
    return _vis_waterfall(
        vis.plot_fit, data, ax, text, label_type, normalize, shift, line_spacing,
        xy_kwargs=xy_kwargs, xycalc_kwargs=xycalc_kwargs, xydiff_kwargs=xydiff_kwargs, xyzero_kwargs=xyzero_kwargs,
        fill_kwargs=fill_kwargs, text_xy=text_xy, line_ind=-4
    )


def modeling():
    return
