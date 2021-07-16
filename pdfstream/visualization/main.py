import itertools
import typing as tp

import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from numpy import ndarray

from pdfstream.visualization.tools import plot_line, plot_fit, normalize, shift, auto_text, set_minor_tick, \
    auto_label

PLOT_METHOD = {
    "line": plot_line,
    "fit": plot_fit
}
TEXT_IND = {
    "line": -1,
    "fit": -4
}


def _waterfall(
    data: ndarray, plot_method: tp.Callable, ax: Axes, normal: bool = True,
    stack: bool = True, gap: float = 0, text: tp.Union[str, None] = None, text_xy: tuple = None,
    text_ind: int = -1, **kwargs
) -> None:
    """The basic visualization function to realize single, waterfall, and comparison plot.

    Parameters
    ----------
    data : ndarray
        The data array. The first row is the independent variable and the following rows are the dependent
        variable.

    plot_method : Callable
        A callable that has the usage like 'plot_method(data: ndarray, ax: Axes, **kwargs)'

    ax : Axes
        The axes to visualize the data. If None, use current axes.

    normal : bool
        If True, the second and the following rows in data will be normalized by (max - min). Else, do nothing.

    stack : bool
        If True, the second and the third rows will be shifted so that there will be a gap between data.

    gap : float
        The gap between the adjacent curves. It is defined by the nearest points in vertical direction.

    text : str
        The text to annotate the curve.

    text_xy : tuple
        The tuple of x and y position of the annotation in data coordinates. If None, use the default in the
        'tools.auto_text'.

    text_ind : int
        The index of the lines in the axes to be annotated after the data is plotted.

    kwargs : optional
        The kwargs arguments for the 'plot_method'.
    """
    if normal:
        data = normalize(data)
    if stack:
        data = shift(data, ax, gap=gap)
    plot_method(data, ax, **kwargs)
    if text is not None:
        auto_text(text, ax, text_xy=text_xy, index=text_ind)
    return


def waterfall(
    dataset: tp.Iterable[ndarray], ax: Axes = None, mode: str = "line", normal: bool = True,
    stack: bool = True, gap: float = 0, texts: tp.Iterable[str] = None, text_xy: tuple = None,
    label: str = None, minor_tick: tp.Union[int, None] = 2, legends: tp.List[str] = None,
    colors: tp.Iterable = None, **kwargs
) -> Axes:
    """The visualization function to realize waterfall, and comparison plot.

    Parameters
    ----------
    dataset :
        A iterable of the data array. The requirement for dimensions depends on the mode.
        If mode = 'line', data = (x_array, y_array)
        If mode = 'fit', data = (x_array, y_array, ycalc_array)

    kwargs :
        The kwargs arguments for the plotting of each data. It depends on mode.
        If mode = 'line', kwargs in ('xy_kwargs',).
        If mode = 'fit', kwargs in ('xy_kwargs', 'xycalc_kwargs', 'xydiff_kwargs', 'xyzero_kwargs',
        'fill_kwargs', 'yzero').

    mode :
        The plotting mode. Currently support 'line', 'fit'.

    ax :
        The axes to visualize the data. If None, use current axes.

    normal :
        If True, the second and the following rows in data will be normalized by (max - min). Else, do nothing.

    stack :
        If True, the second and the third rows will be shifted so that there will be a gap between data (
        waterfall plot). Else, the data will be plotted without shifting (comparison plot).

    gap :
        The gap between the adjacent curves. It is defined by the nearest points in vertical direction.

    texts :
        The texts to annotate the curves. It has the same order as the curves.

    text_xy :
        The tuple of x and y position of the annotation in data coordinates. If None, use the default in the
        'tools.auto_text'.

    label :
        The label type used in automatic labeling. Acceptable types are listed in 'tools._LABELS'

    minor_tick :
        How many parts that the minor ticks separate the space between the two adjacent major ticks. Default 2.
        If None, no minor ticks.

    legends :
        The legend labels for the curves.

    colors :
        The color of the plots. It will be the value for the key 'color' in 'xy_kwargs' in kwargs. If None,
        use default color.

    kwargs :
        The key words for the 'plot_method'. The

    Returns
    -------
    ax : Axes
        The axes with the plot inside.
    """

    def _inject_color(_kwargs, _color):
        if 'xy_kwargs' in _kwargs:
            _kwargs['xy_kwargs'].update({'color': _color})
        else:
            _kwargs['xy_kwargs'] = {'color': _color}
        return

    if ax is None:
        ax = plt.gca()
    if texts is None:
        texts = tuple()
    if colors is None:
        colors = tuple()
    if mode not in PLOT_METHOD:
        raise ValueError(
            "Unknown mode {}. Mode options: {}".format(mode, list(PLOT_METHOD.keys()))
        )
    text_ind = TEXT_IND.get(mode, -1)
    for data, text, color in itertools.zip_longest(dataset, texts, colors):
        if color:
            _inject_color(kwargs, color)
        _waterfall(
            data, PLOT_METHOD[mode], ax=ax, normal=normal, stack=stack, gap=gap, text=text, text_xy=text_xy,
            text_ind=text_ind, **kwargs
        )
    if minor_tick is not None:
        set_minor_tick(ax, minor_tick)
    if label is not None:
        auto_label(ax, label)
    if legends is not None:
        ax.legend(legends)
    return ax


def waterfall_xarray(data: xr.Dataset, x: str, y: str, ycalc: str = None, hue: str = None, **kwargs) -> Axes:
    """The visualization function to realize waterfall, and comparison plot.

    Parameters
    ----------
    data :
        The data set.
        If mode = 'line', data = (x_array, y_array)
        If mode = 'fit', data = (x_array, y_array, ycalc_array)

    xy_kwargs, xycalc_kwargs, xydiff_kwargs, xyzero_kwargs:
        The kwargs arguments for the plotting of each data. It depends on mode.
        If mode = 'line', kwargs in ('xy_kwargs',).
        If mode = 'fit', kwargs in ('xy_kwargs', 'xycalc_kwargs', 'xydiff_kwargs', 'xyzero_kwargs',
        'fill_kwargs', 'yzero').

    ax :
        The axes to visualize the data. If None, use current axes.

    normal :
        If True, the second and the following rows in data will be normalized by (max - min). Else, do nothing.

    stack :
        If True, the second and the third rows will be shifted so that there will be a gap between data (
        waterfall plot). Else, the data will be plotted without shifting (comparison plot).

    gap :
        The gap between the adjacent curves. It is defined by the nearest points in vertical direction.

    texts :
        The texts to annotate the curves. It has the same order as the curves.

    text_xy :
        The tuple of x and y position of the annotation in data coordinates. If None, use the default in the
        'tools.auto_text'.

    label :
        The label type used in automatic labeling. Acceptable types are listed in 'tools._LABELS'

    minor_tick :
        How many parts that the minor ticks separate the space between the two adjacent major ticks. Default 2.
        If None, no minor ticks.

    legends :
        The legend labels for the curves.

    colors :
        The color of the plots. It will be the value for the key 'color' in 'xy_kwargs' in kwargs. If None,
        use default color.

    kwargs :
        The key words for the 'plot_method'. The

    Returns
    -------
    ax : Axes
        The axes with the plot inside.
    """
    dataset = []
    kwargs["mode"] = "fit" if ycalc else "line"
    if hue:
        for i in range(data.dims[hue]):
            sel_data = data.isel({hue: i})
            xy = [sel_data[x].values, sel_data[y].values]
            if ycalc:
                xy.append(sel_data[ycalc].values)
            dataset.append(xy)
    else:
        xy = [data[x].values, data[y].values]
        if ycalc:
            xy.append(data[ycalc].values)
        dataset.append(xy)
    return waterfall(dataset, **kwargs)


def visualize(
    data: ndarray, ax: Axes = None, mode: str = "line", normal: bool = False,
    text: str = None, text_xy: tuple = None, label: str = None,
    minor_tick: int = 2, legends: tp.List[str] = None, color: tp.Any = None, **kwargs
) -> Axes:
    """The visualization function to realize single plot.

    Parameters
    ----------
    data :
        A data array. The requirement for dimensions depends on the mode.
        If mode = 'line', data = (x_array, y_array)
        If mode = 'fit', data = (x_array, y_array, ycalc_array)

    kwargs :
        The kwargs arguments for the plotting of each data. It depends on mode.
        If mode = 'line', kwargs in ('xy_kwargs',).
        If mode = 'fit', kwargs in ('xy_kwargs', 'xycalc_kwargs', 'xydiff_kwargs', 'xyzero_kwargs',
        'fill_kwargs', 'yzero').

    mode :
        The plotting mode. Currently support 'line', 'fit'.

    ax :
        The axes to visualize the data. If None, use current axes.

    normal :
        If True, the second and the following rows in data will be normalized by (max - min). Else, do nothing.

    text :
        The text to annotate the curve.

    text_xy :
        The tuple of x and y position of the annotation in data coordinates. If None, use the default in the
        'tools.auto_text'.

    label :
        The label type used in automatic labeling. Acceptable types are listed in 'tools._LABELS'

    minor_tick : int
        How many parts that the minor ticks separate the space between the two adjacent major ticks. Default 2.
        If None, no minor ticks.

    legends :
        The legend label for the curve.

    color :
        The color of the plots. If None, use default color cycle in rc.

    Returns
    -------
    ax :
        The axes with the plot inside.
    """
    return waterfall(
        (data,), ax=ax, mode=mode, normal=normal, texts=(text,), text_xy=text_xy,
        label=label, minor_tick=minor_tick, stack=False,
        legends=legends if legends else None,
        colors=(color,), **kwargs
    )
