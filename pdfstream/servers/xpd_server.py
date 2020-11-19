"""The analysis server. Process raw image to PDF."""
import typing as tp
from collections import namedtuple

import databroker
from bluesky.callbacks.zmq import RemoteDispatcher
from databroker.v2 import Broker
from event_model import RunRouter
from ophyd.sim import NumpySeqHandler

from pdfstream.callbacks.basic import StartStopCallback
from pdfstream.servers import CONFIG_DIR, ServerNames
from pdfstream.vend.qt_kicker import install_qt_kicker
from .base import run_server, ServerConfig, find_cfg_file
from ..callbacks.analysis import AnalysisConfig, VisConfig, ExportConfig, AnalysisStream, Exporter, Visualizer
from ..callbacks.calibration import CalibrationConfig, Calibration


class XPDConfig(AnalysisConfig, VisConfig, ExportConfig, CalibrationConfig):
    """The configuration for the xpd data reduction. It consists of analysis, visualization and exportation."""

    def __init__(self, *args, **kwargs):
        super(XPDConfig, self).__init__(*args, **kwargs)
        self._an_db = None

    @property
    def an_db(self) -> tp.Union[None, Broker]:
        name = self.get("DATABASE", "an_db", fallback=None)
        if name:
            self._an_db = databroker.catalog[name]
        return self._an_db

    @an_db.setter
    def an_db(self, db: Broker):
        self._an_db = db

    @property
    def functionality(self):
        tup = namedtuple(
            "functionality",
            [
                "do_calibration",
                "dump_to_db",
                "export_files",
                "visualize_data"
            ]
        )
        return tup(
            self.getboolean("FUNCTIONALITY", "do_calibration"),
            self.getboolean("FUNCTIONALITY", "dump_to_db"),
            self.getboolean("FUNCTIONALITY", "export_files"),
            self.getboolean("FUNCTIONALITY", "visualize_data")
        )


class XPDServerConfig(XPDConfig, ServerConfig):
    """The configuration for xpd server."""
    pass


class XPDServer(RemoteDispatcher):
    """The server of XPD data analysis. It is a live dispatcher with XPDRouter subscribed."""

    def __init__(self, config: XPDServerConfig):
        super(XPDServer, self).__init__(config.address, prefix=config.prefix)
        self.subscribe(XPDRouter(config))
        self.subscribe(StartStopCallback())
        install_qt_kicker(self.loop)


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
        find_cfg_file(CONFIG_DIR, ServerNames.xpd)
    config = XPDServerConfig()
    config.read(cfg_file)
    server = XPDServer(config)
    run_server(server)


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
        if self.func.dump_to_db:
            self.analysis.subscribe(self.config.an_db.v1.insert)
        if self.func.export_files:
            self.analysis.subscribe(Exporter(config))
        if self.func.visualize_data:
            self.analysis.subscribe(Visualizer(config))
        if self.func.do_calibration:
            self.calibration = Calibration(config)

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name == "start":
            if doc.get(self.config.dark_identifier, False):
                # dark frame run
                return [], []
            elif doc.get(self.config.calib_identifier, False):
                # calibration run
                if self.func.do_calibration:
                    return [self.calibration], []
                else:
                    return [], []
            else:
                # light frame run
                return [self.analysis], []
        return [], []
