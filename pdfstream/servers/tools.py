from configparser import ConfigParser

from bluesky.callbacks.zmq import RemoteDispatcher


class ServerConfig(ConfigParser):
    """The configuration for the server."""

    @property
    def address(self):
        return self.get("SERVER", "address")

    @property
    def prefix(self):
        return self.get("SERVER", "prefix", fallback="").encode()


def run_server(dispatcher: RemoteDispatcher):
    """Run the server."""
    try:
        print("Start the server. To terminate the server, press 'CTRL + C'.")
        dispatcher.start()
    except KeyboardInterrupt:
        print("Terminate the server.")
