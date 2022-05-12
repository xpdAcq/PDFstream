import typing as T

from pdfstream.callbacks.config import Config
from pdfstream.callbacks.datakeys import DataKeys
from pdfstream.callbacks.imageplotter import ImagePlotter
from pdfstream.callbacks.scatterplotter import ScatterPlotter
from pdfstream.callbacks.waterfallplotter import WaterfallPlotter
from pdfstream.units import LABELS
import pdfstream.io as io


class VisualizationPipeline:
    """The pipeline for the visualization of image, XRD and PDF data."""

    def __init__(self, config: Config, stream_name: str = "primary") -> None:
        self._config: Config = config
        self._stream_name: str = stream_name
        self._descriptor: str = ""
        self._datakeys: T.List[DataKeys] = [DataKeys(d, f) for d, f in zip(config.detectors, config.image_fields)]
        self._image_plotters: T.List[ImagePlotter] = list()
        self._waterfall_plotters: T.List[WaterfallPlotter] = list()
        self._scatter_plotters: T.List[ScatterPlotter] = list()
        self._populate_image_plotters()
        self._populate_waterfall_plotters()
        self._populate_scatter_plotters()

    def _populate_image_plotters(self) -> None:
        exports = self._config.visualizers
        save = self._config.save_plots
        if "image" in exports:
            for dk in self._datakeys:
                image_plotter = ImagePlotter(dk.image, name=dk.image, save=save)
                self._image_plotters.append(image_plotter)
        if "masked_image" in exports:
            for dk in self._datakeys:
                image_plotter = ImagePlotter(dk.image, dk.mask, name=("masked_" + dk.image), save=save)
                self._image_plotters.append(image_plotter)
        return

    def _populate_waterfall_plotters(self) -> None:
        exports = self._config.visualizers
        save = self._config.save_plots
        keys = ["chi_2theta", "chi", "iq", "fq", "sq", "gr"]
        xs = ["chi_2theta", "chi_Q", "iq_Q", "fq_Q", "sq_Q", "gr_r"]
        ys = ["chi_I", "chi_I", "iq_I", "fq_F", "sq_S", "gr_G"]
        labels = [LABELS.chi, LABELS.tth, LABELS.iq, LABELS.fq, LABELS.sq, LABELS.gr]
        names = ["Chi(2theta)", "Chi(Q)", "I(Q)", "F(Q)", "S(Q)", "G(r)"]
        for key, x, y, label, name in zip(keys, xs, ys, labels, names):
            if key in exports:
                for dk in self._datakeys:
                    x_field = getattr(dk, x)
                    y_field = getattr(dk, y)
                    plotter = WaterfallPlotter(x_field, y_field, *label, name=name, save=save)
                    self._waterfall_plotters.append(plotter)
        return

    def _populate_scatter_plotters(self) -> None:
        exports = self._config.visualizers
        save = self._config.save_plots
        keys = ["gr_argmax", "gr_max", "chi_argmax", "chi_max"]
        ys = ["gr_argmax", "gr_max", "chi_argmax", "chi_max"]
        labels = [LABELS.gr[0], LABELS.gr[1], LABELS.chi[0], LABELS.chi[1]]
        names = ["G_peak_position", "G_peak_height", "Chi_peak_position", "Chi_peak_height"]
        for key, y, label, name in zip(keys, ys, labels, names):
            if key in exports:
                for dk in self._datakeys:
                    y_field = getattr(dk, y)
                    plotter = ScatterPlotter(y_field, ylabel=label, name=name, save=save)
                    self._scatter_plotters.append(plotter)
        return

    def __call__(self, name, doc) -> T.Any:
        for plotter in self._image_plotters:
            plotter(name, doc)
        for plotter in self._waterfall_plotters:
            plotter(name, doc)
        for plotter in self._scatter_plotters:
            plotter(name, doc)
        return
