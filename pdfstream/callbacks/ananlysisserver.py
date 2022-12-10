import typing as T
from multiprocessing import Process

from bluesky.callbacks.zmq import RemoteDispatcher
from pdfstream.callbacks.analysispipeline import AnalysisPipeline
from pdfstream.callbacks.config import Config
from pdfstream.io import server_message

PipeLine = T.ClassVar[Config]


class AnalysisServer(RemoteDispatcher):
    def __init__(self, config: Config) -> None:
        super().__init__(config.outbound_address, prefix=config.raw_data_prefix)
        pipeline = AnalysisPipeline(config)
        self.subscribe(pipeline)

    def start(self) -> None:
        server_message("Start {}.".format(self.__class__.__name__))
        try:
            super().start()
        except KeyboardInterrupt:
            pass
        return


def start(cfg_file: str) -> None:
    config = Config()
    config.read_a_file(cfg_file)
    server = AnalysisServer(config)
    server.start()
    return


def get_process(cfg_file: str) -> Process:
    return Process(target=start, args=(cfg_file,))
