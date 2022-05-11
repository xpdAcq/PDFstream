import typing as T
from bluesky.callbacks.zmq import RemoteDispatcher
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.serializationpipeline import SerializationPipeline
from pdfstream.io import server_message

PipeLine = T.ClassVar[Config]


class SerializationServer(RemoteDispatcher):

    def __init__(self, config: Config) -> None:
        super().__init__(config.outbound_address, prefix=config.analyzed_data_prefix)
        pipeline = SerializationPipeline(config)
        self.subscribe(lambda name, doc: server_message("Secondary server received {}.".format(name)))

    def start(self):
        server_message("Start {}".format(self.__class__.__name__))
        return super().start()


def start(cfg_file: str):
    config = Config()
    config.read_a_file(cfg_file)
    server = SerializationServer(config)
    server.start()
    return
