import typing as tp

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


def replay(run: BlueskyRun) -> tp.Tuple[BlueskyRun, XPDAnalyzerConfig, XPDAnalyzer]:
    """Generate the original data, original configure and the XPD analyzer of it.

    Parameters
    ----------
    run :
        The run containing the processed data.

    Returns
    -------
    raw_run :
        The run containing the raw data.

    config :
        The original configuration.

    analyzer :
        The original analyzer.
    """
    config = XPDAnalyzerConfig()
    raw_run = config.retrieve_original_run(run)
    analyzer = XPDAnalyzer(config)
    return raw_run, config, analyzer
