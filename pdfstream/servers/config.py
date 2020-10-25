from configparser import ConfigParser


class ServerConfig(ConfigParser):
    """The configuration for the server."""

    def address(self):
        return self.get("SERVER", "address")

    def prefix(self):
        return self.get("SERVER", "prefix", fallback="").encode()
