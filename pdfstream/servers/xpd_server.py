"""The analysis server. Process raw image to PDF."""
import typing as tp

import databroker.core
from bluesky.callbacks.zmq import Publisher
from databroker.v1 import Broker
from event_model import RunRouter

import pdfstream.io as io
from pdfstream.callbacks.analysis import AnalysisConfig, VisConfig, ExportConfig, AnalysisStream, Exporter, \
    Visualizer
from pdfstream.callbacks.calibration import CalibrationConfig, Calibration
from pdfstream.servers.base import ServerConfig, BaseServer


class XPDConfig(CalibrationConfig, AnalysisConfig, VisConfig, ExportConfig):
    """The configuration for the xpd data reduction. It consists of analysis, visualization and exportation."""

    def __init__(self, *args, **kwargs):
        super(XPDConfig, self).__init__(*args, **kwargs)
        self.add_section("PUBLISH TO")
        self.add_section("FUNCTIONALITY")

    @property
    def an_db(self) -> str:
        return self.get("DATABASE", "an_db", fallback="")

    @property
    def publisher_config(self) -> dict:
        host = self.get("PUBLISH TO", "host", fallback="localhost")
        port = self.getint("PUBLISH TO", "port", fallback=5567)
        prefix = self.get("PUBLISH TO", "prefix", fallback="an").encode()
        return {
            "address": (host, port),
            "prefix": prefix
        }

    @property
    def functionality(self) -> dict:
        return {
            "do_calibration": self.getboolean("FUNCTIONALITY", "do_calibration", fallback=True),
            "dump_to_db": self.getboolean("FUNCTIONALITY", "dump_to_db", fallback=True),
            "export_files": self.getboolean("FUNCTIONALITY", "export_files", fallback=True),
            "visualize_data": self.getboolean("FUNCTIONALITY", "visualize_data", fallback=True),
            "send_messages": self.getboolean("FUNCTIONALITY", "send_messages", fallback=False)
        }


class XPDServerConfig(ServerConfig, XPDConfig):
    """The configuration for xpd server."""
    pass


class XPDServer(BaseServer):
    """The server of XPD data analysis. It is a live dispatcher with XPDRouter subscribed."""
    def __init__(self, config: XPDServerConfig):
        super(XPDServer, self).__init__(config)
        self.subscribe(XPDRouter(config))


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
    config = XPDServerConfig()
    config.read(cfg_file)
    server = XPDServer(config)
    if config.functionality["visualize_data"] and not test_mode:
        server.install_qt_kicker()
    if not test_mode:
        server.start()


class XPDRouter(RunRouter):
    """A router that contains the callbacks for the xpd data reduction."""

    def __init__(self, config: XPDConfig):
        factory = XPDFactory(config)
        super(XPDRouter, self).__init__(
            [factory],
            handler_registry=databroker.core.discover_handlers()
        )


class XPDFactory:
    """The factory to generate callback for xpd data reduction."""

    def __init__(self, config: XPDConfig):
        self.config = config
        self.functionality = self.config.functionality
        self.analysis = [AnalysisStream(config)]
        self.calibration = [Calibration(config)] if self.functionality["do_calibration"] else []
        if self.functionality["dump_to_db"] and self.config.an_db:
            db = Broker.named(self.config.an_db)
            self.analysis[0].subscribe(db.insert)
        if self.functionality["export_files"]:
            self.analysis[0].subscribe(Exporter(config))
        if self.functionality["visualize_data"]:
            self.analysis[0].subscribe(Visualizer(config))
        if self.functionality["send_messages"]:
            pub_config = self.config.publisher_config
            io.server_message(
                "Data will be published to {}:{} with prefix {}.".format(
                    pub_config["address"][0], pub_config["address"][1], pub_config["prefix"]
                )
            )
            self.analysis[0].subscribe(Publisher(**pub_config))
            if self.calibration:
                self.calibration[0].subscribe(Publisher(**pub_config))

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name == "start":
            if doc.get(self.config.dark_identifier):
                # dark frame run
                io.server_message("Receive a dark frame run. Ignore it.")
                return [], []
            elif doc.get(self.config.calib_identifier):
                # calibration run
                io.server_message("Receive a calibration run. Ready to start the calibration.")
                return self.calibration, []
            else:
                # light frame run
                io.server_message("Receive a measurement run. Ready to start processing the data.")
                return self.analysis, []
        return [], []
