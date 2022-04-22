import copy
import typing as T

from bluesky.callbacks.zmq import Publisher
from databroker.core import discover_handlers
from event_model import DocumentNames, Filler
from pdfstream.callbacks.analyzer import Analyzer
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.darksubtraction import DarkSubtraction
from pdfstream.callbacks.filenamerender import FileNameRender

DocumentPair = T.Tuple[str, dict]
HANDLERS = discover_handlers()


class AnalysisPipeline:
    """The analysis pipeline.

    The pipeline includes a sequence of dark subtraction, a sequence of analyzers and a sequence of 
    publishers. These document routers  are generated based on the `image_fields` and `detectors` 
    in the configuration. Their settings are also determined by the configuration. In default, 
    one pipeline is created for a single run so that the cached data in one run won't affect 
    others.

    Parameters
    ----------
    config : Config
        The configuration of the analysis pipeline.
    """

    def __init__(self, config: Config) -> None:
        self._default_config = config
        self._config = None
        self._filler = None
        self._filename_render = None
        self._dark_subtractions = list()
        self._analyzers = list()
        self._publishers = list()

    def _set_config(self, doc: dict) -> None:
        config = copy.deepcopy(self._default_config)
        config.read_user_config(doc)
        config.read_composition(doc)
        config.read_calibration(doc)
        self._config = config
        return

    def _del_config(self, doc: dict) -> None:
        self._config = None
        return

    def _set_filler(self) -> None:
        config = self._config
        if config.fill:
            self._filler = Filler(HANDLERS)
        return

    def _del_filler(self) -> None:
        self._filler = None
        return

    def _set_filename_render(self):
        config = self._config
        self._filename_render = FileNameRender(config)
        return

    def _del_filename_render(self):
        self._filename_render = None
        return

    def _populate_dark_subtractions(self) -> None:
        config = self._config
        self._dark_subtractions = list()
        for field in config.image_fields:
            self._dark_subtractions.append(
                DarkSubtraction(field)
            )
        return

    def _del_dark_subtractions(self) -> None:
        while self._dark_subtractions:
            self._dark_subtractions.pop()
        return

    def _populate_analyzors(self) -> None:
        config = self._config
        self._analyzers = list()
        for datakeys in config.datakeys_list:
            self._analyzers.append(
                Analyzer(datakeys, config)
            )
        return

    def _del_analyzors(self) -> None:
        while self._analyzers:
            self._analyzers.pop()
        return

    def _populate_publishers(self) -> None:
        config = self._config
        self._publishers = list()
        self._publishers.append(
            Publisher(config.inbound_address, prefix=config.analyzed_data_prefix)
        )
        return

    def _del_publishers(self) -> None:
        while self._publishers:
            self._publishers.pop()
        return

    def __call__(self, name: str, doc: dict) -> DocumentPair:
        doc = dict(doc)  # shallow copy so that we can mutate the doc
        if str(name) == "start":
            self._set_config(doc)
            self._set_filler()
            self._set_filename_render()
            self._populate_dark_subtractions()
            self._populate_analyzors()
            self._populate_publishers()
        if self._filler is not None:
            name, doc = self._filler(name, doc)
        name, doc = self._filename_render(name, doc)
        for dark_subtraction in self._dark_subtractions:
            name, doc = dark_subtraction(name, doc)
        for analyzer in self._analyzers:
            name, doc = analyzer(name, doc)
        for publisher in self._publishers:
            publisher(name, doc)
        if name == DocumentNames.stop:
            self._del_publishers()
            self._del_analyzors()
            self._del_dark_subtractions()
            self._del_filler()
            self._del_filename_render()
            self._del_config()
        return name, doc
