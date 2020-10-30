"""The analysis server. Process raw image to PDF."""
from bluesky.callbacks.zmq import RemoteDispatcher
from databroker.v2 import Broker
from pkg_resources import resource_filename

from pdfstream.pipeline.callbacks import StartStopCallback
from pdfstream.pipeline.core import XPDConfig
from pdfstream.pipeline.core import XPDRouter
from pdfstream.vend.qt_kicker import install_qt_kicker
from .tools import ServerConfig, run_server

CFG = {
    "XPD": resource_filename("pdfstream", "configs/pdf_xpdserver.ini"),
    "PDF": resource_filename("pdfstream", "configs/xpd_xpdserver.ini"),
    "TEST": resource_filename("pdfstream", "configs/test_xpdserver.ini"),
}


class XPDServerConfig(XPDConfig, ServerConfig):
    """The configuration for xpd server."""
    pass


class XPDServer(RemoteDispatcher):
    def __init__(self, config: XPDServerConfig, *, raw_db: Broker = None, an_db: Broker = None):
        super(XPDServer, self).__init__(config.dispatcher_address, prefix=config.prefix)
        self.subscribe(XPDRouter(config, raw_db=raw_db, an_db=an_db))
        self.subscribe(StartStopCallback())
        install_qt_kicker(self.loop)


def load_config(cfg_file: str, test_file_base: str = None) -> XPDServerConfig:
    """Load configuration with test settings."""
    config = XPDServerConfig()
    config.read(cfg_file)
    if test_file_base:
        config.tiff_base = test_file_base
        config.calib_base = test_file_base
    return config


def make_and_run(
    cfg_file: str = "~/.config/acq/xpd_server.ini",
    *,
    suppress_warning: bool = True,
    test_file_base: str = None,
    test_raw_db: Broker = None,
    test_an_db: Broker = None
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

    test_file_base :
        A test tiff base and test calib base option for developers. Usually, a temporary folder.

    test_raw_db :
        A test database option for developers. Usually, a temporary database.

    test_an_db :
        A test database option for developers.  Usually, a temporary database.
    """
    if suppress_warning:
        import warnings
        warnings.simplefilter("ignore")
    config = load_config(cfg_file, test_file_base=test_file_base)
    server = XPDServer(config, raw_db=test_raw_db, an_db=test_an_db)
    run_server(server)
