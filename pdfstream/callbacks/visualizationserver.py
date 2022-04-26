import typing as T
from bluesky.callbacks.zmq import RemoteDispatcher
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.visualizationpipeline import VisualizationPipeline
from pdfstream.vend.qt_kicker import install_qt_kicker

PipeLine = T.ClassVar[Config]


class VisualizationServer:

    def __init__(self, config: Config) -> None:
        self._dispatcher = RemoteDispatcher(config.outbound_address, prefix=config.analyzed_data_prefix)
        pipeline = VisualizationPipeline(config)
        self._dispatcher.subscribe(pipeline)
        install_qt_kicker(self._dispatcher.loop)

    def start(self) -> None:
        self._dispatcher.start()
        return
