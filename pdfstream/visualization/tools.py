"""Visualize the data."""
from typing import Union, Any

import numpy as np
from matplotlib.axes import Axes
from numpy import ndarray

__all__ = [
    'auto_label',
    'auto_text',
    'normalize',
    'plot_line',
    'plot_fit',
    'shift',
    'text_position',
    'set_minor_tick'
]

_LABELS = {
    "xy": (r"Q ($\mathrm{\AA}^{-1}$)", r"I (A. U.)"),
    "chi": (r"Q ($\mathrm{\AA}^{-1}$)", r"I (A. U.)"),
    "iq": (r"Q ($\mathrm{\AA}^{-1}$)", r"I (A. U.)"),
    "sq": (r"Q ($\mathrm{\AA}^{-1}$)", r"S"),
    'fq': (r"Q ($\mathrm{\AA}^{-1}$)", r"F ($\mathrm{\AA}^{-1}$)"),
    "gr": (r"r ($\mathrm{\AA}$)", r"G ($\mathrm{\AA}^{-2}$)"),
    "fgr": (r"r ($\mathrm{\AA}$)", r"G ($\mathrm{\AA}^{-2}$)")
}
_TEXT_XY = (0.8, 0.8)


def normalize(vis_data: ndarray):
    """Normalize the data so that the max(data[n]) - min(data[n]) = 1 for n > 0.

    Parameters
    ----------
    vis_data : ndarray
        The data to visualize. The first row is independent variables and the later rows are dependent variables.
    """
    vis_data = np.copy(vis_data)
    bound = np.max(vis_data[1]) - np.min(vis_data[1])
    if bound > 0:
        vis_data[1:] /= bound
    return vis_data


def shift(vis_data: ndarray, ax: Axes, gap: float = 0, inplace: bool = False):
    """Shift the data so that the max(data[n-1]) - max(data[n]) = line_spacing for n > 1.

    Parameters
    ----------
    vis_data : ndarray
        The data to visualize. The first row is independent variables and the later rows are dependent variables.

    ax : Axes
        The axes to plot the data on.

    gap : float
        The spacing between two adjacent lines.

    inplace : bool
        If True, shift the data inplace. Else, shift the copied data.
    """
    if not inplace:
        vis_data = np.copy(vis_data)
    lines = ax.get_lines()
    if len(lines) > 0:
        last_y = lines[-1].get_ydata()
        y = vis_data[1:]
        vis_data[1:] += np.min(last_y) - np.max(y) - gap
    return vis_data


def plot_line(vis_data: ndarray, ax: Axes, xy_kwargs: dict = None):
    """Plot the first two rows of the data.

    Parameters
    ----------
    vis_data : ndarray
        The data to visualize. The first row is independent variables and the later rows are dependent variables.

    ax : Axes
        The axes to plot the data on.

    xy_kwargs : dict
        The kwargs for the ax.plot().
    """
    if xy_kwargs is None:
        xy_kwargs = {}
    ax.plot(vis_data[0], vis_data[1], **xy_kwargs)
    return ax


def text_position(vis_data: ndarray, text_xy: tuple) -> tuple:
    """Calculate the position of the text in data coordinates."""
    fx, fy = text_xy
    x1, y1 = vis_data[:2]
    xa = (1 - fx) * np.min(x1) + fx * np.max(x1)
    ya = (1 - fy) * np.min(y1) + fy * np.max(y1)
    return xa, ya


def complimentary(color: Union[str, Any]):
    """Return the complimentary color of a color string."""
    if color[0] != "#":
        from matplotlib.colors import to_hex
        hexcolor = to_hex(color)[1:]
    else:
        hexcolor = color[1:]
    # convert the string into hex
    intcolor = int(hexcolor, 16)
    # invert the three bytes
    # as good as substracting each of RGB component by 255(FF)
    comp_color = 0xFFFFFF ^ intcolor
    # convert the color back to hex by prefixing a #
    comp_color = "#{:06X}".format(comp_color)
    # return the result
    return comp_color


def auto_text(text: str, ax: Axes, text_xy: tuple = None, index: int = -1):
    """
    Automatically add the text.

    Parameters
    ----------
    text : str
        The content of the text.

    ax : Axes
        The axes to plot the data on.

    text_xy : tuple
        The relative position. The horizontal bound is the xlim. The vertical is the two curves.

    index : int
        The index of the lines to add text. Default -1 (the last line).
    """
    lines = ax.get_lines()
    if len(lines) == 0:
        return ax
    vis_data = lines[index].get_data()
    color = lines[index].get_color()
    if text_xy is None:
        text_xy = _TEXT_XY
    xy = text_position(vis_data, text_xy)
    ax.annotate(text, xy, ha="left", va="center", color=color)
    return ax


def auto_label(ax: Axes, label_type: str):
    """Automatically label the axes according to the name of the vis_field.

    Parameters
    ----------
    ax : Axes
        The axes to plot the data on.

    label_type : str
        The field in the input dictionary. Its value is the data for visualization.
    """
    if label_type in _LABELS:
        labels = _LABELS.get(label_type)
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
    return ax


def get_yzero(y: ndarray, ycalc: ndarray, ydiff: ndarray) -> ndarray:
    """Get the base line yzero of ydiff so that max(yzero + ydiff) = min(min(y), min(ydiff))"""
    return (min(float(np.min(y)), float(np.min(ycalc))) - float(np.max(ydiff))) * np.ones_like(ydiff)


def plot_fit(vis_data: ndarray, ax: Axes,
             xy_kwargs: dict = None, xycalc_kwargs: dict = None, xydiff_kwargs: dict = None,
             xyzero_kwargs: dict = None, fill_kwargs: dict = None,
             yzero: ndarray = None):
    """Visualize the fit.

    Parameters
    ----------
    vis_data : ndarray
        The data to visualize. The first three rows are independent variable, dependent variable, and fitting.

    ax : Axes
        The axes to plot on.

    xy_kwargs : dict
        The kwargs for plotting the y v.s. x curve.

    xycalc_kwargs : dict
        The kwargs for plotting the ycalc v.s. x curve.

    xydiff_kwargs : dict
        The kwargs for plotting the ydiff v.s. x curve.

    xyzero_kwargs : dict
        The kwargs for plotting the yzero v.s. x curve.

    fill_kwargs : dict
        The kwargs for filling in the area between ydiff and yzero.

    yzero : ndarray
        The base line corresponding to the zero value in ydiff.
    """
    # use the default value if None
    if xyzero_kwargs is None:
        xyzero_kwargs = {}
    if xydiff_kwargs is None:
        xydiff_kwargs = {}
    if xycalc_kwargs is None:
        xycalc_kwargs = {}
    if xy_kwargs is None:
        xy_kwargs = {}
    if fill_kwargs is None:
        fill_kwargs = {}
    # split data
    if len(vis_data.shape) != 2:
        raise ValueError('Invalid data shape: {}. Need 2D data array.'.format(vis_data.shape))
    if vis_data.shape[0] < 3:
        raise ValueError('Invalid data dimension: {}. Need dim >= 3'.format(vis_data.shape[0]))
    x, y, ycalc = vis_data[:3]
    ydiff = y - ycalc
    # shift ydiff
    if yzero is None:
        yzero = get_yzero(y, ycalc, ydiff)
    ydiff += yzero
    # circle data curve
    _xy_kwargs = {'fillstyle': 'none', 'label': 'data'}
    _xy_kwargs.update(xy_kwargs)
    data_line, = ax.plot(x, y, 'o', **_xy_kwargs)
    # solid calculation curve
    _xycalc_kwargs = {'label': 'fit', 'color': complimentary(data_line.get_color())}
    _xycalc_kwargs.update(xycalc_kwargs)
    ax.plot(x, ycalc, '-', **_xycalc_kwargs)
    # dash zero difference curve
    _xyzero_kwargs = {'color': 'grey'}
    _xyzero_kwargs.update(xyzero_kwargs)
    ax.plot(x, yzero, '--', **_xyzero_kwargs)
    # solid shifted difference curve
    _xydiff_kwargs = {'label': 'residuals', 'color': data_line.get_color()}
    _xydiff_kwargs.update(xydiff_kwargs)
    diff_line, = ax.plot(x, ydiff, '-', **_xydiff_kwargs)
    # fill in area between curves
    if fill_kwargs.pop('fill', True):
        _fill_kwargs = {'alpha': 0.4, 'color': diff_line.get_color()}
        _fill_kwargs.update(fill_kwargs)
        ax.fill_between(x, ydiff, yzero, **_fill_kwargs)
    return ax


def set_minor_tick(ax: Axes, n: int = 2):
    """Set one minor tick between major ticks."""
    from matplotlib.ticker import AutoMinorLocator
    ax.xaxis.set_minor_locator(AutoMinorLocator(n))
    ax.yaxis.set_minor_locator(AutoMinorLocator(n))
    return ax
