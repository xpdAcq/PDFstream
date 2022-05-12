from multiprocessing import Process
import typing as T
from bluesky.callbacks.zmq import RemoteDispatcher
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.visualizationpipeline import VisualizationPipeline
from pdfstream.vend.qt_kicker import install_qt_kicker
from pdfstream.io import server_message

PipeLine = T.ClassVar[Config]


class VisualizationServer(RemoteDispatcher):

    def __init__(self, config: Config) -> None:
        super().__init__(config.outbound_address, prefix=config.analyzed_data_prefix)
        pipeline = VisualizationPipeline(config)
        self.subscribe(pipeline)
        install_qt_kicker(self.loop)

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
    server = VisualizationServer(config)
    server.start()
    return


def get_process(cfg_file: str) -> Process:
    return Process(target=start, args=(cfg_file))
