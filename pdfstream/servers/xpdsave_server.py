from pdfstream.callbacks.analysis import ExportConfig, Exporter
from pdfstream.servers import CONFIG_DIR, ServerNames
from pdfstream.servers.base import BaseServer, ServerConfig, find_cfg_file, StartStopCallback


class XPDSaveServerConfig(ServerConfig, ExportConfig):
    """A configuration for the XPDSaveServer."""
    pass


class XPDSaveServer(BaseServer):
    """A server that saves the analyzed data from the xpd server."""

    def __init__(self, config: XPDSaveServerConfig):
        super(XPDSaveServer, self).__init__(config)
        self.subscribe(Exporter(config))
        self.subscribe(StartStopCallback())


def make_and_run(
    cfg_file: str = None,
    *,
    suppress_warning: bool = True,
    test_mode: bool = False
):
    """Run the xpd data reduction server.

    The server will receive message from proxy and process the data in the message. The processed data will be
    visualized and exported to database and the file system.

    Parameters
    ----------
    cfg_file :
        The path to configuration .ini file. The default path is "~/.config/acq/xpd_server.ini".

    suppress_warning :
        If True, all warning will be suppressed. Turn it to False when running in a test.

    test_mode :
        If True, just create a server but not start. Used for test.
    """
    if suppress_warning:
        import warnings
        warnings.simplefilter("ignore")
    if not cfg_file:
        cfg_file = find_cfg_file(CONFIG_DIR, ServerNames.xpdsave)
    config = XPDSaveServerConfig()
    config.read(cfg_file)
    server = XPDSaveServer(config)
    if not test_mode:
        server.start()
