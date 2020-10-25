"""The analysis server. Process raw image to PDF."""
from pdfstream.pipeline.core import XPDConfig
from .config import ServerConfig


class XPDServerConfig(XPDConfig, ServerConfig):
    """The configuration for xpd server."""
    pass


def make_and_run(cfg_file: str = None):
    """Run the xpd data reduction server."""
    pass
