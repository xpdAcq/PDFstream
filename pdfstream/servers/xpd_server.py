"""The analysis server. Process raw image to PDF."""
import typing as tp
from bluesky.callbacks.zmq import RemoteDispatcher
from databroker.v2 import Broker
from event_model import RunRouter
from ophyd.sim import NumpySeqHandler
from pkg_resources import resource_filename

from pdfstream.callbacks.basic import StartStopCallback
from pdfstream.vend.qt_kicker import install_qt_kicker
from .config import ServerConfig
from .tools import run_server
from ..callbacks.analysis import AnalysisConfig, VisConfig, ExportConfig, AnalysisStream, Exporter, Visualizer
from ..callbacks.calibration import CalibrationConfig, Calibration

CFG = {
    "XPD": resource_filename("pdfstream", "configs/pdf_xpdserver.ini"),
    "PDF": resource_filename("pdfstream", "configs/xpd_xpdserver.ini"),
    "TEST": resource_filename("pdfstream", "configs/test_xpdserver.ini"),
}


class XPDConfig(AnalysisConfig, VisConfig, ExportConfig, CalibrationConfig):
    """The configuration for the xpd data reduction. It consists of analysis, visualization and exportation."""

    @property
    def an_db(self) -> tp.Union[None, Broker]:
        name = self.get("DATABASE", "an_db", fallback=None)
        if name:
            from databroker import catalog
            return catalog[name]
        return None


class XPDServerConfig(XPDConfig, ServerConfig):
    """The configuration for xpd server."""
    pass


class XPDServer(RemoteDispatcher):
    def __init__(self, config: XPDServerConfig, *, raw_db: Broker = None, an_db: Broker = None):
        super(XPDServer, self).__init__(config.address, prefix=config.prefix)
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


class XPDFactory:
    """The factory to generate callback for xpd data reduction."""

    def __init__(self, config: XPDConfig, *, raw_db: Broker = None, an_db: Broker = None):
        self.config = config
        self.analysis = AnalysisStream(config, raw_db=raw_db)
        if an_db is not None:
            self.analysis.subscribe(an_db.v1.insert)
        if self.config.an_db is not None:
            self.analysis.subscribe(self.config.an_db.v1.insert)
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


class XPDRouter(RunRouter):
    """A router that contains the callbacks for the xpd data reduction."""

    def __init__(self, config: XPDConfig, *, raw_db: Broker = None, an_db: Broker = None):
        factory = XPDFactory(config, raw_db=raw_db, an_db=an_db)
        super(XPDRouter, self).__init__(
            [factory],
            handler_registry={"NPY_SEQ": NumpySeqHandler}
        )
