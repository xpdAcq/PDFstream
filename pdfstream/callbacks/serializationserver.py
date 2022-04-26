import typing as T
from bluesky.callbacks.zmq import RemoteDispatcher
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.serializationpipeline import SerializationPipeline

PipeLine = T.ClassVar[Config]


class SerializationServer:

    def __init__(self, config: Config) -> None:
        self._dispatcher = RemoteDispatcher(config.outbound_address, prefix=config.analyzed_data_prefix)
        pipeline = SerializationPipeline(config)
        self._dispatcher.subscribe(pipeline)

    def start(self) -> None:
        self._dispatcher.start()
        return
