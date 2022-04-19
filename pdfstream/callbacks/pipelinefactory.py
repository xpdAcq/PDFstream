import copy
from debugpy import configure
from event_model import RunRouter, DocumentNames, Filler
import typing as T
from pdfstream.callbacks.config import Config
from databroker.core import discover_handlers

DocumentPair = T.Tuple[str, dict]
PipeLine = T.ClassVar[Config]
Callback = T.Callable[[str, dict], DocumentPair]
Callbacks = T.List[Callback]
CallbackFactory = T.Callable[[str, dict], Callbacks]
CallbackFactories = T.List[CallbackFactory]


class PipelineFactory:

    def __init__(self, pipeline: PipeLine, config: Config) -> None:
        self._pipeline = pipeline
        self._config = config
        self._updated_config = None

    def _set_updated_config(self, doc: dict) -> None:
        config = copy.deepcopy(self._config)
        config.read_user_config(doc)
        config.read_composition(doc)
        self._updated_config = config
        return

    def __call__(self, name: str, doc: dict) -> T.Tuple[Callbacks, CallbackFactories]:
        if name == DocumentNames.start:
            self._set_updated_config(doc)
            pipeline = self._pipeline(self._updated_config)
            return [pipeline], []
        return [], []
