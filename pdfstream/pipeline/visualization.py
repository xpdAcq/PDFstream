import matplotlib.pyplot as plt
import numpy as np
import typing as tp
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.callbacks.broker import LiveImage
from bluesky.callbacks.core import CallbackBase
from xpdview.waterfall import Waterfall

from pdfstream.pipeline.units import LABELS


def gen_vis_cbs() -> tp.Generator:
    """Generate the visualization callbacks for the Visualizer of analyzed data."""
    yield BestEffortCallback(table_enabled=False)
    yield LiveMaskedImage("dk_sub_image", "mask", cmap="viridis")
    yield LiveWaterfall("chi_Q", "chi_I", labels=LABELS.chi)
    yield LiveWaterfall("fq_Q", "fq_F", labels=LABELS.fq)
    yield LiveWaterfall("gr_r", "gr_G", labels=LABELS.gr)


class LiveMaskedImage(LiveImage):
    """Live image show of a image with a mask."""

    def __init__(self, field: str, msk_field: str, *, cmap: str, norm: tp.Callable = None,
                 limit_func: tp.Callable = None, auto_draw: bool = True, interpolation: str = None,
                 window_title: str = None):
        self.msk_field = msk_field
        super(LiveMaskedImage, self).__init__(
            field, cmap=cmap, norm=norm, limit_func=limit_func,
            auto_redraw=auto_draw, interpolation=interpolation, window_title=window_title
        )

    def event(self, doc):
        super(LiveImage, self).event(doc)
        data = np.ma.masked_array(doc["data"][self.field], doc["data"][self.msk_field])
        self.update(data)


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
