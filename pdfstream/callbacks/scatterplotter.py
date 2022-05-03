import typing as T
from pathlib import Path

import matplotlib.pyplot as plt
from bluesky.callbacks import CallbackBase
from bluesky.callbacks.mpl_plotting import LivePlot, LiveScatter
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import pdfstream.io as io


class ScatterPlotter(CallbackBase):
    """Scatter plot of the quantity of intests."""

    def __init__(self, y: str, *, ax: Axes = None, ylabel: str = None, name: str = "scatter", save: bool = False, suffix: str = ".png", **kwargs):
        super(ScatterPlotter, self).__init__()
        if ax is None:
            _, ax = plt.subplots()
        kwargs.setdefault("marker", "o")
        self.y_field = y
        self.name = name
        self.save = save
        self.suffix = suffix
        self._fig = ax.get_figure()
        self._ax = ax
        self._ylabel = ylabel
        self._kwargs = kwargs
        self._callback = None
        self._directory = None
        self._filename = ""

    @property
    def figure(self) -> Figure:
        return self._fig

    def _get_hints(self, doc: dict) -> T.List[str]:
        hints = []
        dims = doc.get("hints", {}).get("dimensions", [])
        for data_keys, stream_name in dims:
            if stream_name == "primary":
                hints.extend(data_keys)
        return hints

    def savefig(self) -> None:
        if self._filename is None:
            io.server_message("No filename.")
            return
        if self._directory is None:
            io.server_message("No direcory.")
            return
        f = self._filename + "_" + self.name + self.suffix
        fpath = self._directory.joinpath(f)
        self.figure.savefig(fpath)
        return

    def start(self, doc):
        self._ax.cla()
        indeps = self._get_hints(doc)
        if len(indeps) == 1:
            self._callback = LivePlot(self.y_field, x=indeps[0], ax=self._ax, **self._kwargs)
        elif len(indeps) == 2:
            self._callback = LiveScatter(*indeps, self.y_field, ax=self._ax, **self._kwargs)
        else:
            self._callback = LivePlot(self.y_field, x="time", ax=self._ax, **self._kwargs)
        self._callback.start(doc)
        if self.save:
            if "filename" in doc:
                self._filename = doc["filename"]
            else:
                io.server_message("No 'filename' in start.")
                return doc
            if "directory" in doc:
                self._directory = Path(doc["directory"]).joinpath("plots")
                self._directory.mkdir(exist_ok=True, parents=True)
            else:
                io.server_message("No 'direcory' in start.")
        return

    def descriptor(self, doc):
        self._callback.descriptor(doc)
        return

    def event(self, doc):
        if int(doc["seq_num"]) == 1:
            self._ax.clear()
        self._callback.event(doc)
        if self._ylabel:
            self._ax.set_ylabel(self._ylabel)
            self._fig.canvas.draw_idle()
        return

    def stop(self, doc):
        self._callback.stop(doc)
        if self.save:
            self.savefig()
        return
    