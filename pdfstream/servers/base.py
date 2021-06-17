import typing
from configparser import ConfigParser

from bluesky.callbacks import CallbackBase
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

    def read(self, filenames, encoding=None) -> typing.List[str]:
        returned = super(ServerConfig, self).read(filenames, encoding=encoding)
        if not returned:
            raise FileNotFoundError("No such configuration file {}".format(filenames))
        return returned


class BaseServer(RemoteDispatcher):
    """The basic server class."""

    def __init__(self, config: ServerConfig):
        super(BaseServer, self).__init__(config.address, prefix=config.prefix)
        self._config = config

    def start(self):
        try:
            server_message(
                "Server is started. " +
                "Listen to {}:{} prefix {}.".format(self._config.host, self._config.port, self._config.prefix)
            )
            super(BaseServer, self).start()
        except KeyboardInterrupt:
            server_message("Server is terminated.")

    def install_qt_kicker(self):
        install_qt_kicker(self.loop)


class StartStopCallback(CallbackBase):
    """Print the time for analysis"""

    def __init__(self):
        super(StartStopCallback, self).__init__()

    def start(self, doc):
        server_message("Receive the start of run {}".format(doc["uid"]))
        return super(StartStopCallback, self).start(doc)

    def descriptor(self, doc):
        server_message("Receive the stream {}.".format(doc["name"]))
        return super(StartStopCallback, self).descriptor(doc)

    def event(self, doc):
        server_message("Receive the event {}.".format(doc["seq_num"]))
        return super(StartStopCallback, self).event(doc)

    def event_page(self, doc):
        server_message("Receive the event page.")
        return super(StartStopCallback, self).event_page(doc)

    def stop(self, doc):
        server_message("Receive the stop of run {}".format(doc.get("run_start", "")))
        return super(StartStopCallback, self).stop(doc)
