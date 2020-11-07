from configparser import ConfigParser


class ServerConfig(ConfigParser):
    """The configuration for the server."""

    @property
    def host(self):
        return self.get("PROXY", "host")

    @property
    def address(self):
        return self.host, self.out_port

    @property
    def in_port(self):
        return self.getint("PROXY", "in_port")

    @property
    def out_port(self):
        return self.getint("PROXY", "out_port")

    @property
    def prefix(self):
        return self.get("PROXY", "prefix", fallback="").encode()
