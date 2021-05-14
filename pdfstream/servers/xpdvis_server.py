from pdfstream.callbacks.analysis import Visualizer, VisConfig
from pdfstream.servers import CONFIG_DIR, ServerNames
from pdfstream.servers.base import BaseServer, ServerConfig, find_cfg_file
from pdfstream.servers.base import StartStopCallback


class XPDVisServerConfig(VisConfig, ServerConfig):
    """A configuration for the XPDVisServer."""
    pass


class XPDVisServer(BaseServer):
    """A server that visualizes the analyzed data from the xpd server."""

    def __init__(self, config: XPDVisServerConfig):
        super(XPDVisServer, self).__init__(config.address, prefix=config.prefix)
        self.subscribe(StartStopCallback())
        self.subscribe(Visualizer(config))


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
        cfg_file = find_cfg_file(CONFIG_DIR, ServerNames.xpdvis)
    config = XPDVisServerConfig()
    config.read(cfg_file)
    server = XPDVisServer(config)
    if not test_mode:
        server.install_qt_kicker()
        server.start()
