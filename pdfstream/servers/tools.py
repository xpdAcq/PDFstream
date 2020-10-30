from configparser import ConfigParser

from bluesky.callbacks.zmq import RemoteDispatcher


class ServerConfig(ConfigParser):
    """The configuration for the server."""

    @property
    def address(self):
        return self.get("PROXY", "address")

    @property
    def dispatcher_address(self):
        return self.address, self.out_port

    @property
    def in_port(self):
        return self.getint("PROXY", "in_port")

    @property
    def out_port(self):
        return self.getint("PROXY", "out_port")

    @property
    def prefix(self):
        return self.get("PROXY", "prefix", fallback="").encode()


def run_server(dispatcher: RemoteDispatcher):
    """Run the server."""
    try:
        print("Start the server. To terminate the server, press 'CTRL + C'.")
        dispatcher.start()
    except KeyboardInterrupt:
        print("Terminate the server.")
