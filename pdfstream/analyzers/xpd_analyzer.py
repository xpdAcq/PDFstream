import typing as tp

from databroker import catalog
from databroker.core import BlueskyRun

from pdfstream.analyzers.base import AnalyzerConfig, Analyzer
from pdfstream.servers.xpd_server import XPDRouter, XPDConfig


class XPDAnalyzerConfig(XPDConfig, AnalyzerConfig):
    """The configuration of the XPDAnalyzer."""
    pass


class XPDAnalyzer(XPDRouter, Analyzer):
    """The class to process the XPD data to PDF data. """
    pass


def replay(run: BlueskyRun) -> tp.Tuple[XPDAnalyzerConfig, XPDAnalyzer]:
    """Generate the original data, original configure and the XPD analyzer of it.

    Parameters
    ----------
    run :
        The run containing the processed data.

    Returns
    -------
    config :
        The original configuration.

    analyzer :
        The original analyzer.
    """
    config = XPDAnalyzerConfig()
    config.read_run(run)
    analyzer = XPDAnalyzer(config)
    return config, analyzer


def retrieve_original_run(run: BlueskyRun) -> tp.Union[None, BlueskyRun]:
    """Retrieve the original run."""
    start = run.metadata['start']
    if 'original_run_uid' not in start:
        raise Warning("Missing original_run_uid. Cannot retrieve original run.")
    if 'original_db' not in start:
        raise Warning("Missing original_db. Cannot retrieve original run.")
    try:
        db = catalog[start['original_db']]
    except KeyError:
        raise Warning("Missing {} in catalog. Cannot retrieve original run.".format(start['original_db']))
    try:
        return db[start['original_run_uid']]
    except KeyError:
        raise Warning("Run {} not found in database.".format(start['original_run_uid']))
