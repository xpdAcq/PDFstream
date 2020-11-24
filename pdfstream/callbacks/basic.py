import typing as tp
from pathlib import Path

import numpy as np
import pandas as pd
from bluesky.callbacks import CallbackBase
from bluesky.callbacks.best_effort import LivePlot, LiveScatter
from bluesky.callbacks.broker import LiveImage
from databroker.v2 import Broker
from event_model import unpack_event_page
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.widgets import Slider
from xpdview.waterfall import Waterfall

import pdfstream.callbacks.from_descriptor as fd
import pdfstream.callbacks.from_start as fs
from pdfstream.vend.formatters import SpecialStr


class ArrayExporter(CallbackBase):
    """An base class for the callbacks to find and export the 1d array."""
    file_suffix = ""
    file_stem = "{descriptor[name]}-{field}-{event[seq_num]}"

    def __init__(self, directory: str, *, file_prefix: str, data_keys: tp.List[str] = None):
        super(ArrayExporter, self).__init__()
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.file_template = SpecialStr(
            file_prefix + self.file_stem + self.file_suffix
        )
        self.data_keys = data_keys
        self.start_doc = None
        self.descriptor_doc = None

    def start(self, doc):
        self.start_doc = doc
        super(ArrayExporter, self).start(doc)

    def descriptor(self, doc):
        if not self.data_keys:
            self.data_keys = list(fd.yield_1d_array(doc["data_keys"]))
        self.descriptor_doc = doc
        super(ArrayExporter, self).descriptor(doc)

    def event(self, doc):
        self.export(doc)
        super(ArrayExporter, self).event(doc)

    def event_page(self, doc):
        for event in unpack_event_page(doc):
            self.event(event)

    def stop(self, doc):
        self.start_doc = None
        self.descriptor_doc = None
        super(ArrayExporter, self).stop(doc)

    def export(self, doc):
        pass


class NumpyExporter(ArrayExporter):
    """An exporter to export the 1d array data in .npy file."""
    file_suffix = ".npy"

    def export(self, doc):
        for data_key in self.data_keys:
            arr: np.ndarray = doc["data"][data_key]
            filename = self.file_template.format(start=self.start_doc, descriptor=self.descriptor_doc, event=doc,
                                                 field=data_key)
            filepath = self.directory.joinpath(filename)
            np.save(str(filepath), arr)


class DataFrameExporter(ArrayExporter):
    """An exporter to export data in a dataframe in the .csv file."""
    file_suffix = ".csv"

    def export(self, doc):
        _data = {data_key: pd.Series(doc["data"][data_key]) for data_key in self.data_keys}
        df = pd.DataFrame(data=_data)
        filename = self.file_template.format(start=self.start_doc, descriptor=self.descriptor_doc, event=doc,
                                             field="data")
        filepath = self.directory.joinpath(filename)
        df.to_csv(str(filepath))


class MyLiveImage(LiveImage):
    """A customized LiveImage."""

    def show(self):
        self.cs._fig.show()


class LiveMaskedImage(MyLiveImage):
    """Live image show of a image with a mask."""

    def __init__(self, field: str, msk_field: str, *, cmap: str, norm: tp.Callable = None,
                 limit_func: tp.Callable = None, auto_draw: bool = True, interpolation: str = None,
                 window_title: str = None, db: Broker = None):
        self.msk_field = msk_field
        super(LiveMaskedImage, self).__init__(
            field, cmap=cmap, norm=norm, limit_func=limit_func,
            auto_redraw=auto_draw, interpolation=interpolation, window_title=window_title, db=db
        )

    def event(self, doc):
        super(LiveImage, self).event(doc)
        data = np.ma.masked_array(doc["data"][self.field], doc["data"][self.msk_field])
        self.update(data)


class MyWaterfall(Waterfall):
    """An adaptation of WaterFall. Allow using ax instead of Figure."""

    def __init__(self, *, xlabel: str, ylabel: str, ax: Axes, **kwargs):
        super(Waterfall, self).__init__()
        self.ax = ax
        self.fig = self.ax.figure
        self.canvas = self.fig.canvas
        self.kwargs = kwargs
        self.x_array_list = []
        self.y_array_list = []

        # callback for showing legend
        self.canvas.mpl_connect("pick_event", self.on_plot_hover)
        self.key_list = []
        self.unit = (xlabel, ylabel)

        # add sliders, which store information
        self.ydist = 0
        self.xdist = 0

        y_offset_slider_ax = self.fig.add_axes([0.15, 0.95, 0.25, 0.035])
        self.y_offset_slider = Slider(
            y_offset_slider_ax,
            "y-offset",
            0.0,
            1.0,
            valinit=0.1,
            valfmt="%1.2f",
        )
        self.y_offset_slider.on_changed(self.update_y_offset)

        x_offset_slider_ax = self.fig.add_axes([0.6, 0.95, 0.25, 0.035])
        self.x_offset_slider = Slider(
            x_offset_slider_ax,
            "x-offset",
            0.0,
            1.0,
            valinit=0.,
            valfmt="%1.2f",
        )
        self.x_offset_slider.on_changed(self.update_x_offset)


class LiveWaterfall(CallbackBase):
    """A live water plot for the one dimensional data."""

    def __init__(self, x: str, y: str, *, xlabel: str, ylabel: str, ax: Axes, **kwargs):
        """Initiate the instance.

        Parameters
        ----------
        x :
            The key of the independent variable.

        y :
            The key of the dependent variable.

        xlabel :
            The tuple of the labels of x shown in the figure.

        ylabel :
            The tuple of the labels of y shown in the figure.

        ax :
            The axes to plot.

        kwargs :
            The kwargs for the matplotlib.pyplot.plot.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.ax = ax
        self.waterfall = MyWaterfall(xlabel=xlabel, ylabel=ylabel, ax=self.ax, **kwargs)

    def start(self, doc):
        super(LiveWaterfall, self).start(doc)
        self.waterfall.clear()

    def event(self, doc):
        super(LiveWaterfall, self).event(doc)
        x_data = doc["data"][self.x]
        y_data = doc["data"][self.y]
        key = doc['seq_num']
        self.update(key, (x_data, y_data))

    def update(self, key: str, int_data: tp.Tuple[np.ndarray, np.ndarray]):
        self.waterfall.update(key_list=[key], int_data_list=[int_data])

    def show(self):
        self.ax.figure.show()


class SmartScalarPlot(CallbackBase):
    """A plot for scalar variable. Use LivePlot for one dimensional case and Use LiveScatter for two dimensional
    case """

    def __init__(self, y: str, *, ax: Axes = None, ylabel: str = None, **kwargs):
        super(SmartScalarPlot, self).__init__()
        self.y = y
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        self.ax = ax
        self.ylabel = ylabel
        self.kwargs = kwargs
        self.callback = None

    def start(self, doc):
        super(SmartScalarPlot, self).start(doc)
        self.clear()
        indeps = fs.get_indeps(doc, exclude={"time"})
        if len(indeps) == 1:
            self.callback = LivePlot(self.y, x=indeps.pop(), ax=self.ax, **self.kwargs)
        elif len(indeps) == 2:
            self.callback = LiveScatter(indeps.pop(), indeps.pop(), self.y, ax=self.ax, **self.kwargs)
        else:
            self.callback = LivePlot(self.y, ax=self.ax, **self.kwargs)
        self.callback.start(doc)

    def descriptor(self, doc):
        super(SmartScalarPlot, self).descriptor(doc)
        self.callback.descriptor(doc)

    def event(self, doc):
        super(SmartScalarPlot, self).event(doc)
        self.callback.event(doc)
        if self.ylabel:
            self.ax.set_ylabel(self.ylabel)

    def stop(self, doc):
        super(SmartScalarPlot, self).stop(doc)
        self.callback.stop(doc)

    def clear(self):
        self.ax.cla()
        self.callback = None

    def show(self):
        self.ax.figure.show()
