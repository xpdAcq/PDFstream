import typing as tp
from event_model import RunRouter
from ophyd.sim import NumpySeqHandler

from .analysis import AnalysisConfig, AnalysisStream
from .export import ExportConfig, Exporter
from .visualization import VisConfig, Visualizer


class XPDConfig(AnalysisConfig, VisConfig, ExportConfig):
    """The configuration for the xpd data reduction. It consists of analysis, visualization and exportation."""
    pass


class XPDRouter(RunRouter):
    """A router that contains the callbacks for the xpd data reduction."""

    def __init__(self, config: XPDConfig):
        factory = XPDFactory(config)
        super(XPDRouter, self).__init__(
            [factory],
            handler_registry={"NPY_SEQ": NumpySeqHandler}
        )


class XPDFactory:
    """The factory to generate callback for xpd data reduction."""

    def __init__(self, config: XPDConfig):
        self.config = config
        self.dispatcher = AnalysisStream(config)
        self.dispatcher.subscribe(Exporter(config))
        self.dispatcher.subscribe(Visualizer(config))

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name != "start" or doc.get(self.config.dark_identifier, False):
            return [], []
        return [self.dispatcher], []
