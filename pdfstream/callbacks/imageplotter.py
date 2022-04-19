import typing as T
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from bluesky.callbacks import CallbackBase
from matplotlib.figure import Figure
from xray_vision.backend.mpl.cross_section_2d import CrossSection


class ImagePlotter(CallbackBase):
    """Live image show of a image with a mask."""

    def __init__(self, image_field: str, mask_field: str = None, *, cmap: str = "viridis", norm: T.Callable = None,
                 limit_func: T.Callable = None, auto_redraw: bool = True, interpolation: str = None,
                 window_title: str = None, name: str = "image"):
        fig = plt.figure()
        self.image_field = image_field
        self.mask_field = mask_field
        self.name = name
        self._uid = None
        self._cs = CrossSection(fig, cmap, norm,
                                limit_func, auto_redraw, interpolation)
        if window_title:
            self._cs._fig.canvas.set_window_title(window_title)
        self._cs._fig.show()

    def start(self, doc: dict):
        self._uid = doc["uid"]
        return doc

    @property
    def figure(self) -> Figure:
        return self._cs._fig

    def update(self, data: np.ndarray) -> None:
        self._cs.update_image(data)
        self.figure.canvas.draw_idle()
        return

    def _get_filename(self, seq_num: int) -> Path:
        items = [self._uid, self.image_field]
        if self.mask_field is not None:
            items.append("with")
            items.append(self.mask_field)
        items.append(str(seq_num))
        return Path("_".join(items)).with_suffix(".npg")

    def event(self, doc):
        if self.mask_field in doc["data"]:
            data_arr = np.ma.masked_array(
                doc["data"][self.image_field],
                doc["data"][self.mask_field]
            )
        else:
            data_arr = np.array(doc["data"][self.image_field])
        self.update(data_arr)
        return doc
