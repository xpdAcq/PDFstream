import typing as T
from pathlib import Path

import numpy as np
from bluesky.callbacks import CallbackBase
from matplotlib.figure import Figure
from xpdview.waterfall import Waterfall as OldWaterfall
import pdfstream.io as io


class Waterfall(OldWaterfall):

    def _update_plot(self) -> None:
        """core method to update x-, y-offset sliders"""
        x_offset_val = self.x_offset_slider.val
        y_offset_val = self.y_offset_slider.val

        # update matplotlib line data
        lines = self.ax.get_lines()
        for i, (l, x, y) in enumerate(
            zip(lines, self.x_array_list, self.y_array_list)
        ):
            xx = x + self.xdist * i * x_offset_val
            yy = y + self.ydist * i * y_offset_val
            l.set_data(xx, yy)
        self.ax.relim()
        self.ax.autoscale()
        if self.unit:
            xlabel, ylabel = self.unit
            self.ax.set_xlabel(xlabel)
            self.ax.set_ylabel(ylabel)
        self.canvas.draw_idle()
        return


class WaterfallPlotter(CallbackBase):
    """A live waterfall plot for the two columns data."""

    def __init__(self, x: str, y: str, xlabel: str, ylabel: str, name: str = "waterfall", save: bool = False, suffix: str = ".png", **kwargs):
        super().__init__()
        self.x_field = x
        self.y_field = y
        self.name = name
        self.save = save
        self.suffix = suffix
        self._directory = None
        self._filename = ""
        self._waterfall = Waterfall(unit=(xlabel, ylabel), **kwargs)

    @property
    def figure(self) -> Figure:
        return self._waterfall.fig

    def update(self, key: str, int_data: T.Tuple[np.ndarray, np.ndarray]):
        self._waterfall.update(key_list=[key], int_data_list=[int_data])
        return

    def savefig(self) -> None:
        if self._filename is None:
            io.server_message("Filename is not specified.")
            return
        if self._directory is None:
            io.server_message("Directory is not specified.")
            return
        f = self._filename + "_" + self.name + self.suffix
        fpath = self._directory.joinpath(f)
        self.figure.savefig(fpath)
        return

    def start(self, doc):
        if self.save:
            if "filename" in doc:
                self._filename = doc["filename"]
            else:
                io.server_message("No 'filename' in doc.")
                return doc
            if "directory" in doc:
                self._directory = Path(doc["directory"]).joinpath("plots")
                self._directory.mkdir(exist_ok=True, parents=True)
            else:
                io.server_message("No 'directory' in doc.")
        return doc

    def event(self, doc):
        if self.x_field not in doc["data"]:
            io.server_message("No '{}' in the data.".format(self.x_field))
            return doc
        if self.y_field not in doc["data"]:
            io.server_message("No '{}' in the data.".format(self.y_field))
            return doc
        if int(doc['seq_num']) == 0:
            # clear the old data at the first new event
            self._waterfall.clear()
            self.figure.show()
        x_data = doc["data"][self.x_field]
        y_data = doc["data"][self.y_field]
        key = doc['seq_num']
        self.update(key, (x_data, y_data))
        return doc

    def stop(self, doc):
        if self.save:
            self.savefig()
        return doc
