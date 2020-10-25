from event_model import RunRouter

from .analysis import AnalysisConfig
from .export import ExportConfig
from .visualization import VisConfig


class XPDFConfig(AnalysisConfig, VisConfig, ExportConfig):
    """The configuration for the xpd data reduction. It consists of analysis, visualization and exportation."""
    pass


class XPDRouter(RunRouter):
    """A router that contains the callbacks for the xpd data reduction."""
    pass


class XPDFactory:
    """The factory to generate callback for xpd data reduction."""
    pass
