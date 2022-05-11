import typing as T
from pathlib import Path

import numpy as np
from bluesky.callbacks import CallbackBase
from matplotlib.figure import Figure
from xpdview.waterfall import Waterfall as OldWaterfall
import pdfstream.io as io

from .plotterbase import PlotterBase

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
        return


class WaterfallPlotter(PlotterBase):
    """A live waterfall plot for the two columns data."""

    def __init__(self, x: str, y: str, xlabel: str, ylabel: str, name: str = "waterfall", save: bool = False, suffix: str = ".png", **kwargs):
        self.x_field = x
        self.y_field = y
        self._waterfall = Waterfall(unit=(xlabel, ylabel), **kwargs)
        super().__init__(name, self._waterfall.fig, suffix=suffix, save_at_stop=save)

    def update(self, key: str, int_data: T.Tuple[np.ndarray, np.ndarray]):
        self._waterfall.update(key_list=[key], int_data_list=[int_data])
        return

    def plot_event(self, doc):
        if self.x_field not in doc["data"]:
            io.server_message("No '{}' in the data.".format(self.x_field))
            return doc
        if self.y_field not in doc["data"]:
            io.server_message("No '{}' in the data.".format(self.y_field))
            return doc
        if int(doc['seq_num']) == 1:
            # clear the old data at the first new event
            self._waterfall.clear()
        x_data = doc["data"][self.x_field]
        y_data = doc["data"][self.y_field]
        key = doc['seq_num']
        self.update(key, (x_data, y_data))
        return
