from configparser import ConfigParser, Error
from datetime import datetime
from pathlib import Path

from bluesky.callbacks.zmq import RemoteDispatcher

from pdfstream.vend.qt_kicker import install_qt_kicker


class ServerConfig(ConfigParser):
    """The configuration for the server."""

    @property
    def host(self):
        return self.get("PROXY", "host")

    @property
    def address(self):
        return self.host, self.port

    @property
    def port(self):
        return self.getint("PROXY", "port")

    @property
    def prefix(self):
        return self.get("PROXY", "prefix", fallback="").encode()


class BaseServer(RemoteDispatcher):
    """The basic server class."""

    def start(self):
        super(BaseServer, self).start()
        print("[{}] Server is started".format(datetime.now()))

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
