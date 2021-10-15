import copy
import typing as tp
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from bluesky.callbacks import CallbackBase
from bluesky.callbacks.best_effort import LivePlot, LiveScatter
from bluesky.callbacks.broker import LiveImage
from databroker.v2 import Broker
from event_model import unpack_event_page
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.widgets import Slider
from pyFAI.io.ponifile import PoniFile
from suitcase.tiff_series import Serializer as TiffSerializer
from xpdview.waterfall import Waterfall

import pdfstream.callbacks.from_descriptor as fd
import pdfstream.callbacks.from_start as fs
import pdfstream.io as io
from pdfstream.vend.formatters import SpecialStr


class ArrayExporter(CallbackBase):
    """An base class for the callbacks to find and export the 1d array."""
    _file_suffix = ""
    _file_stem = "{descriptor[name]}-{field}-{event[seq_num]}"

    def __init__(self, directory: str, *, file_prefix: str, data_keys: list = None):
        super(ArrayExporter, self).__init__()
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._file_prefix = file_prefix
        self._file_template = ""
        self.data_keys = data_keys
        self.start_doc = {}
        self.descriptor_doc = {}
        self._indeps = set()
        self._indep2unit = {}

    def start(self, doc):
        self.start_doc = doc
        self._indeps = fs.get_indeps(doc, exclude={"time"})
        super(ArrayExporter, self).start(doc)

    def descriptor(self, doc):
        if not self.data_keys:
            self.data_keys = list(fd.yield_1d_array(doc["data_keys"]))
        self.descriptor_doc = doc
        self._indep2unit = fd.get_units(doc["data_keys"], self._indeps)
        super(ArrayExporter, self).descriptor(doc)

    def event(self, doc):
        indep_str = fd.get_indep_str(doc["data"], self._indep2unit)
        self._file_template = SpecialStr(
            self._file_prefix + indep_str + self._file_stem + self._file_suffix
        )
        self.export(doc)
        super(ArrayExporter, self).event(doc)

    def event_page(self, doc):
        for event in unpack_event_page(doc):
            self.event(event)

    def stop(self, doc):
        super(ArrayExporter, self).stop(doc)

    def export(self, doc):
        pass


class NumpyExporter(ArrayExporter):
    """An exporter to export the array data one by one in .npy file."""
    _file_suffix = ".npy"

    def export(self, doc):
        for data_key in self.data_keys:
            arr: np.ndarray = doc["data"][data_key]
            filename = self._file_template.format(start=self.start_doc, descriptor=self.descriptor_doc, event=doc,
                                                  field=data_key)
            filepath = self.directory.joinpath(filename)
            np.save(str(filepath), arr)


class StackedNumpyExporter(ArrayExporter):
    """An exporter to export the column-stacked array data in .npy file."""
    _file_suffix = ".npy"

    def export(self, doc):
        arr: np.ndarray = np.stack([doc["data"][data_key] for data_key in self.data_keys], axis=-1)
        field = "_".join(self.data_keys)
        filename = self._file_template.format(start=self.start_doc, descriptor=self.descriptor_doc, event=doc,
                                              field=field)
        filepath = self.directory.joinpath(filename)
        np.save(str(filepath), arr)


class StackedNumpyTextExporter(CallbackBase):
    """An base class for the callbacks to find and export the 1d array."""
    _file_stem = "{descriptor[name]}-{event[seq_num]}"

    def __init__(self, file_prefix: str, *args, no_single_value: bool = True):
        """Args are sequences of 'directory to export', 'data keys to combine', 'file suffix'."""
        super(StackedNumpyTextExporter, self).__init__()
        self._no_single_value = no_single_value
        self._file_prefix = file_prefix
        self._file_template = ""
        self.directories = tuple(map(Path, args[::3]))
        self.data_keys = args[1::3]
        self.file_suffixes = args[2::3]
        self.start_doc = {}
        self.descriptor_doc = {}
        self._indeps = set()
        self._indep2unit = {}

    def start(self, doc):
        self.start_doc = doc
        self._indeps = fs.get_indeps(doc, exclude={"time"})
        super(StackedNumpyTextExporter, self).start(doc)

    def descriptor(self, doc):
        self.descriptor_doc = doc
        self._indep2unit = fd.get_units(doc["data_keys"], self._indeps)
        super(StackedNumpyTextExporter, self).descriptor(doc)

    def event(self, doc):
        indep_str = fd.get_indep_str(doc["data"], self._indep2unit)
        self._file_template = SpecialStr(
            self._file_prefix + indep_str + self._file_stem
        )
        self.export(doc)
        super(StackedNumpyTextExporter, self).event(doc)

    def event_page(self, doc):
        for event in unpack_event_page(doc):
            self.event(event)

    def stop(self, doc):
        super(StackedNumpyTextExporter, self).stop(doc)

    def export(self, doc):
        for directory, data_key_tup, file_suffix in zip(self.directories, self.data_keys, self.file_suffixes):
            arr: np.ndarray = np.stack([doc["data"][data_key] for data_key in data_key_tup], axis=-1)
            if arr.ndim == 2 and arr.shape[0] <= 1 and self._no_single_value:
                continue
            filename = self._file_template.format(start=self.start_doc, descriptor=self.descriptor_doc, event=doc)
            filename += file_suffix
            directory.mkdir(exist_ok=True, parents=True)
            filepath = directory.joinpath(filename)
            header = " ".join(data_key_tup)
            np.savetxt(str(filepath), arr, header=header)


class DataFrameExporter(ArrayExporter):
    """An exporter to export data in a dataframe in the .csv file."""
    _file_suffix = ".csv"

    def export(self, doc):
        _data = {data_key: pd.Series(doc["data"][data_key]) for data_key in self.data_keys}
        df = pd.DataFrame(data=_data)
        filename = self._file_template.format(start=self.start_doc, descriptor=self.descriptor_doc, event=doc,
                                              field="data")
        filepath = self.directory.joinpath(filename)
        df.to_csv(str(filepath))


class MyLiveImage(LiveImage):
    """A customized LiveImage."""

    def update(self, data):
        data_arr = np.asarray(data)
        super(MyLiveImage, self).update(data_arr)

    def show(self):
        self.cs._fig.show()


class LiveMaskedImage(LiveImage):
    """Live image show of a image with a mask."""

    def __init__(self, field: str, msk_field: str, *, cmap: str, norm: tp.Callable = None,
                 limit_func: tp.Callable = None, auto_draw: bool = True, interpolation: str = None,
                 window_title: str = None, db: Broker = None):
        self.msk_field = msk_field
        self.msk_array = None
        super(LiveMaskedImage, self).__init__(
            field, cmap=cmap, norm=norm, limit_func=limit_func,
            auto_redraw=auto_draw, interpolation=interpolation, window_title=window_title, db=db
        )

    def event(self, doc):
        super(LiveImage, self).event(doc)
        data_arr = np.ma.masked_array(doc["data"][self.field], doc["data"][self.msk_field])
        self.update(data_arr)

    def show(self):
        self.cs._fig.show()


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
        self.ax.cla()
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
        self.callback.event(doc, )
        if self.ylabel:
            self.ax.set_ylabel(self.ylabel)

    def stop(self, doc):
        super(SmartScalarPlot, self).stop(doc)
        self.callback.stop(doc, )

    def clear(self):
        self.ax.cla()
        self.callback = None

    def show(self):
        self.ax.figure.show()


class MyTiffSerializer(TiffSerializer):
    """A TiffSerializer that allows specific data keys to be exported."""

    def __init__(self, directory, file_prefix: SpecialStr, data_keys=None, astype='uint32',
                 bigtiff=False, byteorder=None, imagej=False, **kwargs):
        super(MyTiffSerializer, self).__init__(directory, file_prefix=file_prefix, astype=astype,
                                               bigtiff=bigtiff, byteorder=byteorder, imagej=imagej, **kwargs)
        self.data_keys = data_keys
        self._indeps = frozenset()
        self._indep2unit = dict()

    def start(self, doc):
        self._indeps = fs.get_indeps(doc, exclude={"time"})
        return super(MyTiffSerializer, self).start(doc)

    def descriptor(self, doc):
        self._indep2unit = fd.get_units(doc["data_keys"], self._indeps)
        return super(MyTiffSerializer, self).descriptor(doc)

    def event(self, doc):
        # add indep
        _file_prefix = copy.copy(self._file_prefix)
        indep_str = fd.get_indep_str(doc["data"], self._indep2unit)
        self._file_prefix = SpecialStr(_file_prefix + indep_str)
        # select data key
        if not self.data_keys:
            returned = super(MyTiffSerializer, self).event(doc)
        else:
            doc = dict(doc)
            doc["data"] = {k: v for k, v in doc["data"].items() if k in self.data_keys}
            returned = super(MyTiffSerializer, self).event(doc)
        # go back to original data key
        self._file_prefix = _file_prefix
        return returned


class CalibrationExporter(CallbackBase):
    """Export the calibration metadata in poni file."""

    def __init__(self, directory: str, file_prefix: str = "start[uid]_", md_key: str = "calibration_md"):
        super(CalibrationExporter, self).__init__()
        self._directory = Path(directory).expanduser()
        self._directory.mkdir(exist_ok=True, parents=True)
        self._file_prefix = SpecialStr(file_prefix)
        self._md_key = md_key
        self._directory.mkdir(exist_ok=True, parents=True)

    def start(self, doc):
        if self._md_key in doc:
            calibration_md = doc[self._md_key]
            pf = PoniFile()
            pf.read_from_dict(calibration_md)
            file_prefix = self._file_prefix.format(start=doc)
            file_name = file_prefix.strip("_")
            file_path = self._directory.joinpath(file_name).with_suffix(".poni")
            with file_path.open("w") as f:
                pf.write(f)
        else:
            io.server_message("Missing 'calibration_md' in the start.")
        return super(CalibrationExporter, self).start(doc)


class YamlSerializer(CallbackBase):
    """Export the start document in yaml file."""

    def __init__(self, directory: str, file_prefix: str = "start[uid]_"):
        super(YamlSerializer, self).__init__()
        self._directory = Path(directory).expanduser()
        self._directory.mkdir(exist_ok=True, parents=True)
        self._file_prefix = file_prefix

    def start(self, doc):
        file_prefix = self._file_prefix.format(start=doc)
        filename = file_prefix.strip("_")
        file_path = self._directory.joinpath(filename).with_suffix(".yaml")
        with file_path.open("w") as f:
            yaml.dump(doc, f)
        return super(YamlSerializer, self).start(doc)
