"""The analysis server. Process raw image to PDF."""
import typing as tp

import databroker
from bluesky.callbacks.zmq import Publisher
from databroker.v2 import Broker
from event_model import RunRouter
from ophyd.sim import NumpySeqHandler

from pdfstream.callbacks.analysis import AnalysisConfig, VisConfig, ExportConfig, AnalysisStream, Exporter, \
    Visualizer, no_need_to_refresh_db
from pdfstream.callbacks.calibration import CalibrationConfig, Calibration
from pdfstream.servers import CONFIG_DIR, ServerNames
from pdfstream.servers.base import ServerConfig, find_cfg_file, BaseServer, StartStopCallback


class XPDConfig(AnalysisConfig, VisConfig, ExportConfig, CalibrationConfig):
    """The configuration for the xpd data reduction. It consists of analysis, visualization and exportation."""

    def __init__(self, *args, **kwargs):
        super(XPDConfig, self).__init__(*args, **kwargs)
        self._an_db = None

    @property
    def an_db(self) -> tp.Union[None, Broker]:
        name = self.get("DATABASE", "an_db", fallback=None)
        if no_need_to_refresh_db(self._an_db, name):
            pass
        elif name is None:
            self._an_db = None
        elif name == "temp":
            print("Warning: a temporary db is created for an db. It will be destroy at the end of the session.")
            self._an_db = databroker.v2.temp()
        else:
            self._an_db = databroker.catalog[name]
        return self._an_db

    @an_db.setter
    def an_db(self, db: Broker):
        section_name = "DATABASE"
        db_key = "an_db"
        if section_name not in self.sections():
            self.add_section(section_name)
        self.set(section_name, db_key, db.name)
        self._an_db = db

    @property
    def publisher_config(self) -> dict:
        host = self.get("PUBLISH TO", "host")
        port = self.getint("PUBLISH TO", "port")
        prefix = self.get("PUBLISH TO", "prefix", fallback="").encode()
        return {
            "address": (host, port),
            "prefix": prefix
        }

    @property
    def functionality(self) -> dict:
        return {
            "do_calibration": self.getboolean("FUNCTIONALITY", "do_calibration"),
            "dump_to_db": self.getboolean("FUNCTIONALITY", "dump_to_db"),
            "export_files": self.getboolean("FUNCTIONALITY", "export_files"),
            "visualize_data": self.getboolean("FUNCTIONALITY", "visualize_data"),
            "send_messages": self.getboolean("FUNCTIONALITY", "send_messages"),
        }


class XPDServerConfig(XPDConfig, ServerConfig):
    """The configuration for xpd server."""
    pass


class XPDServer(BaseServer):
    """The server of XPD data analysis. It is a live dispatcher with XPDRouter subscribed."""
    def __init__(self, config: XPDServerConfig):
        super(XPDServer, self).__init__(config.address, prefix=config.prefix)
        self.subscribe(StartStopCallback())
        self.subscribe(XPDRouter(config))


def make_and_run(
    cfg_file: str = None,
    *,
    suppress_warning: bool = True
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
    """
    if suppress_warning:
        import warnings
        warnings.simplefilter("ignore")
    if not cfg_file:
        cfg_file = find_cfg_file(CONFIG_DIR, ServerNames.xpd)
    config = XPDServerConfig(allow_no_value=True)
    config.read(cfg_file)
    server = XPDServer(config)
    server.install_qt_kicker()
    server.start()


class XPDRouter(RunRouter):
    """A router that contains the callbacks for the xpd data reduction."""

    def __init__(self, config: XPDConfig):
        factory = XPDFactory(config)
        super(XPDRouter, self).__init__(
            [factory],
            handler_registry={"NPY_SEQ": NumpySeqHandler}
        )


class XPDFactory:
    """The factory to generate callback for xpd data reduction."""

    def __init__(self, config: XPDConfig):
        self.config = config
        self.analysis = AnalysisStream(config)
        self.func = self.config.functionality
        if self.func["do_calibration"]:
            self.calibration = Calibration(config)
        if self.func["dump_to_db"]:
            self.analysis.subscribe(self.config.an_db.v1.insert)
        if self.func["export_files"]:
            self.analysis.subscribe(Exporter(config))
        if self.func["visualize_data"]:
            self.analysis.subscribe(Visualizer(config))
        if self.func["send_messages"]:
            self.analysis.subscribe(Publisher(**self.config.publisher_config))

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name == "start":
            if doc.get(self.config.dark_identifier):
                # dark frame run
                return [], []
            elif doc.get(self.config.calib_identifier):
                # calibration run
                if self.func.do_calibration:
                    return [self.calibration], []
                else:
                    return [], []
            else:
                # light frame run
                return [self.analysis], []
        return [], []
