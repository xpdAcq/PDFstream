from configparser import ConfigParser, Error
from pathlib import Path

from bluesky.callbacks.zmq import RemoteDispatcher


def run_server(dispatcher: RemoteDispatcher):
    """Run the server."""
    try:
        print("Start the server. To terminate the server, press 'CTRL + C'.")
        dispatcher.start()
    except KeyboardInterrupt:
        print("Terminate the server.")


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


def find_cfg_file(directory: Path, name: str) -> str:
    """Find the configuration file by matching the value of BASIC section name paramter to the name variable."""
    for filename in directory.glob("*.ini"):
        config = ConfigParser()
        try:
            config.read(str(filename))
            _name = config["BASIC"]["name"]
            if name == _name:
                return str(filename)
        except Error:
            continue
    raise FileNotFoundError("No .ini file in {} satisfies [BASIC][name] == {}".format(str(directory), name))