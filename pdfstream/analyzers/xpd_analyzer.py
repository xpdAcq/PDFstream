from pdfstream.analyzers.base import AnalyzerConfig, Analyzer
from pdfstream.servers.xpd_server import XPDRouter, XPDConfig


class XPDAnalyzerConfig(XPDConfig, AnalyzerConfig):
    """The configuration of the XPDAnalyzer."""
    pass


class XPDAnalyzer(XPDRouter, Analyzer):
    """The class to process the XPD data to PDF data. """
    pass
