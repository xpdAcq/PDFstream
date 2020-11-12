import numpy as np
import time
import typing as tp
from bluesky.callbacks import CallbackBase
from bluesky.callbacks.broker import LiveImage
from databroker.v2 import Broker
from event_model import unpack_event_page
from matplotlib import pyplot as plt
from pathlib import Path
from xpdview.waterfall import Waterfall

try:
    from diffpy.pdfgetx import PDFConfig, PDFGetter
except ImportError:
    pass


class StartStopCallback(CallbackBase):
    """Print the time for analysis"""

    def __init__(self):
        super().__init__()
        self.t0 = 0

    def start(self, doc):
        self.t0 = time.time()
        print("START ANALYSIS ON {}".format(doc["uid"]))

    def stop(self, doc):
        print("FINISH ANALYSIS ON {}".format(doc.get("run_start", "NA")))
        print("Analysis time {}".format(time.time() - self.t0))


class NumpyExporter(CallbackBase):
    """An exporter to export the array data in .npy file."""

    def __init__(self, directory: str, file_prefix: str, data_keys: tp.List[str]):
        super(NumpyExporter, self).__init__()
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.file_template = file_prefix + "{data_key}-{event[seq_num]}.npy"
        self.data_keys = data_keys
        self.cache = dict()

    def start(self, doc):
        self.cache = dict()
        self.cache["start"] = doc
        super(NumpyExporter, self).start(doc)

    def event_page(self, doc):
        for event in unpack_event_page(doc):
            self.event(event)

    def event(self, doc):
        for data_key in self.data_keys:
            arr: np.ndarray = doc["data"][data_key]
            filename = self.file_template.format(start=self.cache["start"], event=doc, data_key=data_key)
            filepath = self.directory.joinpath(filename)
            np.save(str(filepath), arr)
        super(NumpyExporter, self).event(doc)

    def stop(self, doc):
        self.cache = dict()
        super(NumpyExporter, self).stop(doc)


class LiveMaskedImage(LiveImage):
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


class LiveWaterfall(CallbackBase):
    """A live water plot for the one dimensional data."""

    def __init__(self, x: str, y: str, *, xlabel: str, ylabel: str, **kwargs):
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

        kwargs :
            The kwargs for the matplotlib.pyplot.plot.
        """
        super().__init__()
        self.x = x
        self.y = y
        fig = plt.figure()
        self.waterfall = Waterfall(fig=fig, unit=(xlabel, ylabel), **kwargs)
        fig.show()

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
