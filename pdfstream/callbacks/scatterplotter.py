import typing as T
from pathlib import Path

import matplotlib.pyplot as plt
from bluesky.callbacks import CallbackBase
from bluesky.callbacks.mpl_plotting import LivePlot, LiveScatter
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import pdfstream.io as io

from .plotterbase import PlotterBase

class ScatterPlotter(PlotterBase):
    """Scatter plot of the quantity of intests."""

    def __init__(self, y: str, *, ylabel: str = None, name: str = "scatter", save: bool = False, suffix: str = ".png", **kwargs):
        fig, ax = plt.subplots()
        kwargs.setdefault("marker", "o")
        self.y_field = y
        self._ax = ax
        self._ylabel = ylabel
        self._kwargs = kwargs
        self._callback = None
        super().__init__(name, fig, save_at_stop=save, suffix=suffix)

    def _get_hints(self, doc: dict) -> T.List[str]:
        hints = []
        dims = doc.get("hints", {}).get("dimensions", [])
        for data_keys, stream_name in dims:
            if stream_name == "primary":
                hints.extend(data_keys)
        return hints

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
        return super().start(doc)

    def descriptor(self, doc):
        if doc["name"] == self._stream_name:
            self._callback.descriptor(doc)
        return super().descriptor(doc)

    def plot_event(self, doc):
        if self.y_field not in doc["data"]:
            return
        self._callback.event(doc)
        if self._ylabel:
            self._ax.set_ylabel(self._ylabel)
        self._updated = True
        return

    def stop(self, doc):
        self._callback.stop(doc)
        return super().stop(doc)
