import typing as tp

from databroker.v2 import Broker
from event_model import RunRouter
from ophyd.sim import NumpySeqHandler

from .analysis import AnalysisConfig, AnalysisStream
from .calibration import CalibrationConfig, Calibration
from .export import ExportConfig, Exporter
from .visualization import VisConfig, Visualizer


class XPDConfig(AnalysisConfig, VisConfig, ExportConfig, CalibrationConfig):
    """The configuration for the xpd data reduction. It consists of analysis, visualization and exportation."""
    pass


class XPDRouter(RunRouter):
    """A router that contains the callbacks for the xpd data reduction."""

    def __init__(self, config: XPDConfig, *, raw_db: Broker = None):
        factory = XPDFactory(config, raw_db=raw_db)
        super(XPDRouter, self).__init__(
            [factory],
            handler_registry={"NPY_SEQ": NumpySeqHandler}
        )


class XPDFactory:
    """The factory to generate callback for xpd data reduction."""

    def __init__(self, config: XPDConfig, *, raw_db: Broker = None):
        self.config = config
        self.analysis = AnalysisStream(config, raw_db=raw_db)
        self.analysis.subscribe(Exporter(config))
        self.analysis.subscribe(Visualizer(config))
        self.calibration = Calibration(config, raw_db=raw_db)

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name == "start":
            if doc.get(self.config.dark_identifier):
                # dark frame run
                return [], []
            elif doc.get(self.config.calib_identifier):
                # calibration run
                return [self.calibration], []
            else:
                # light frame run
                return [self.analysis], []
        return [], []
