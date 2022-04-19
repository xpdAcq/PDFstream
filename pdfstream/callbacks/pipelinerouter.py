import copy
from debugpy import configure
from event_model import RunRouter, Filler
import typing as T
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.pipelinefactory import PipelineFactory
from databroker.core import discover_handlers

PipeLine = T.ClassVar[Config]


class PipelineRouter(RunRouter):

    def __init__(self, pipeline: PipeLine, config: Config, fill: bool = False):
        factories = [PipelineFactory(pipeline, config)]
        if fill:
            super().__init__(factories, discover_handlers(), filler_class=Filler, fill_or_fail=True)
        else:
            super().__init__(factories)
