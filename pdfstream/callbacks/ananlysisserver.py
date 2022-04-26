from asyncore import dispatcher
import typing as T
from bluesky.callbacks.zmq import RemoteDispatcher
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.analysispipeline import AnalysisPipeline

PipeLine = T.ClassVar[Config]

class AnalysisServer:

    def __init__(self, config: Config) -> None:
        self._dispatcher = RemoteDispatcher(config.outbound_address, prefix=config.raw_data_prefix)
        pipeline = AnalysisPipeline(config)
        self._dispatcher.subscribe(pipeline)

    def start(self) -> None:
        self._dispatcher.start()
        return
