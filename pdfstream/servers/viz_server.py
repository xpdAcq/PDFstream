"""The visualization server. Visualize the data yield from analysis server."""
import numpy as np
import typing as tp
from bluesky.callbacks.broker import LiveImage
from bluesky.callbacks.zmq import RemoteDispatcher
from configparser import ConfigParser
from event_model import RunRouter
from xpdview.callbacks import LiveWaterfall

import pdfstream.pipeline.callbacks as callbacks


class VizServerConfig(ConfigParser):
    """The configuration of the visualization server."""

    @property
    def cmap(self):
        section = self["IMAGE SETTING"]
        return section.get("cmap")

    @property
    def alpha(self):
        section = self["IMAGE SETTING"]
        return section.getfloat("alpha")

    @property
    def in_address(self):
        return self.get("DISPATCHER", "address")

    @property
    def in_prefix(self):
        return self.get("DISPATCHER", "prefix")


def limit_func(arr: np.ndarray, alpha: float) -> tp.Tuple[float, float]:
    mean = np.mean(arr)
    std = np.std(arr)
    return mean - alpha * std, mean + alpha * std


def make_router(config: VizServerConfig) -> RunRouter:
    """Make the run router of the visualization server. It will visualize scalar plot, waterfall plot, and image
    from the run that is not dark run."""

    def factory(name, doc):
        if name == "start":
            analysis_stage = doc.get("analysis_stage")
            if analysis_stage == callbacks.AutoMasking.__name__:
                live_image = LiveImage(
                    "masked_img",
                    cmap=config.cmap,
                    limit_func=lambda x: limit_func(x, config.alpha)
                )
                return [live_image], []
            if analysis_stage in frozenset(
                [
                    callbacks.AzimuthalIntegration.__name__,
                    callbacks.TransformIQtoFQ.__name__,
                    callbacks.TransformFQtoGr.__name__
                ]
            ):
                water_fall = LiveWaterfall()
                return [water_fall], []
        return [], []

    # currently all docs are filled, no need for handler
    return RunRouter([factory])


def make_dispatcher(cfg_file: str) -> RemoteDispatcher:
    """Make the remote dispatcher of visualization server based on the configuration file."""
    pass


def make_and_run(cfg_file: str):
    """Make the visualization server and run it."""
    pass
