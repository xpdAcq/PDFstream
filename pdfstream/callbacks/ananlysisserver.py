import typing as T
from bluesky.callbacks.zmq import RemoteDispatcher
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.analysispipeline import AnalysisPipeline
from pdfstream.io import server_message

PipeLine = T.ClassVar[Config]

class AnalysisServer(RemoteDispatcher):

    def __init__(self, config: Config) -> None:
        super().__init__(config.outbound_address, prefix=config.raw_data_prefix)
        pipeline = AnalysisPipeline(config)
        self.subscribe(pipeline)

    def start(self):
        server_message("Start {}".format(self.__class__.__name__))
        return super().start()
