from databroker.core import BlueskyRun

from pdfstream.analyzers.base import AnalyzerConfig, Analyzer
from pdfstream.servers.xpd_server import XPDRouter, XPDConfig


class XPDAnalyzerConfig(XPDConfig, AnalyzerConfig):
    """The configuration of the XPDAnalyzer."""

    def retrieve_original_run(self, run: BlueskyRun) -> BlueskyRun:
        """Retrieve the original run."""
        self.read_run(run)
        uid = run.metadata['start']['original_run_uid']
        return self.raw_db[uid]


class XPDAnalyzer(XPDRouter, Analyzer):
    """The class to process the XPD data to PDF data. """
    pass
