from configparser import ConfigParser, Error
from pathlib import Path

from bluesky.callbacks import CallbackBase
from bluesky.callbacks.core import make_class_safe
from bluesky.callbacks.zmq import RemoteDispatcher

from pdfstream.io import server_message
from pdfstream.vend.qt_kicker import install_qt_kicker


class ServerConfig(ConfigParser):
    """The configuration for the server."""

    def __init__(self, *args, **kwargs):
        super(ServerConfig, self).__init__(*args, **kwargs)
        self.add_section("LISTEN TO")

    @property
    def host(self):
        return self.get("LISTEN TO", "host", fallback="localhost")

    @property
    def port(self):
        return self.getint("LISTEN TO", "port", fallback=5568)

    @property
    def address(self):
        return self.host, self.port

    @property
    def prefix(self):
        return self.get("LISTEN TO", "prefix", fallback="raw").encode()


class BaseServer(RemoteDispatcher):
    """The basic server class."""

    def start(self):
        try:
            server_message("Server is started.")
            super(BaseServer, self).start()
        except KeyboardInterrupt:
            server_message("Server is terminated.")

    def install_qt_kicker(self):
        install_qt_kicker(self.loop)


def find_cfg_file(directory: Path, name: str) -> str:
    """Find the configuration file by matching the value of BASIC section name paramter to the name variable."""
    ini_files = []
    for filename in directory.glob("*.ini"):
        try:
            config = ConfigParser()
            ini_files.extend(config.read(str(filename)))
            if name == config["BASIC"]["name"]:
                return str(filename)
        except Error:
            continue
    raise FileNotFoundError(
        "\n".join(
            [
                "These are the ini_files found in the {}:".format(str(directory)),
                "\n".join(ini_files),
                "No .ini file satisfies that parameter 'name = {}' in section [BASIC]".format(name)
            ]
        )
    )


@make_class_safe
class StartStopCallback(CallbackBase):
    """Print the time for analysis"""

    def __init__(self):
        super(StartStopCallback, self).__init__()

    def start(self, doc):
        server_message("Receive the start of run {}".format(doc["uid"]))
        super(StartStopCallback, self).start(doc)

    def stop(self, doc):
        server_message("Receive the stop of run {}".format(doc.get("run_start", "")))
        super(StartStopCallback, self).stop(doc)
