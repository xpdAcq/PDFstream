import matplotlib.pyplot as plt
import numpy as np
import typing as tp
from bluesky.callbacks.broker import LiveImage
from bluesky.callbacks.core import CallbackBase
from configparser import ConfigParser
from event_model import RunRouter
from xpdview.waterfall import Waterfall

from pdfstream.pipeline.units import LABELS


class VisConfig(ConfigParser):
    """The configuration for the visualization."""

    @property
    def masked_image_setting(self):
        section = self["MASKED IMAGE VISUALIZATION"]
        return {
            "cmap": section.get("cmap")
        }


class Visualizer(RunRouter):
    """A run router for visualization of the analyzed data"""

    def __init__(self, config: VisConfig, handler_registry: dict = None):
        self.cb_lst = [
            LiveImage(
                "masked_image",
                cmap=config.masked_image_setting["cmap"]
            ),
            LiveWaterfall("chi_Q", "chi_I", labels=LABELS.chi),
            LiveWaterfall("fq_Q", "fq_F", labels=LABELS.fq),
            LiveWaterfall("gr_r", "gr_G", labels=LABELS.gr)
        ]
        super().__init__([lambda *x: (self.cb_lst, [])], handler_registry=handler_registry)


class LiveWaterfall(CallbackBase):
    """A live water plot for the one dimensional data."""

    def __init__(self, x: str, y: str, *, labels: tp.Tuple[str, str], **kwargs):
        """Initiate the instance.

        Parameters
        ----------
        x :
            The key of the independent variable.

        y :
            The key of the dependent variable.

        labels :
            The tuple of the labels of x and y shown in the figure.

        kwargs :
            The kwargs for the matplotlib.pyplot.plot.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.kwargs = kwargs
        self.labels = labels
        self.waterfall = None

    def start(self, doc):
        fig = plt.figure()
        self.waterfall = Waterfall(fig=fig, unit=self.labels, **self.kwargs)

    def event(self, doc):
        x_data = doc["data"][self.x]
        y_data = doc["data"][self.y]
        key = doc['seq_num']
        self.update(key, (x_data, y_data))

    def update(self, key: str, int_data: tp.Tuple[np.ndarray, np.ndarray]):
        self.waterfall.update(key_list=[key], int_data_list=[int_data])

    def stop(self, doc):
        self.waterfall = None
