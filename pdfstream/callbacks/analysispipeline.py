import typing as T

from bluesky.callbacks.zmq import Publisher
from pdfstream.callbacks.analyzer import Analyzer
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.darksubtraction import DarkSubtraction
from pdfstream.callbacks.datakeys import DataKeys

DocumentPair = T.Tuple[str, dict]


class AnalysisPipeline:

    def __init__(self, config: Config) -> None:
        self._config = config
        self._dark_subtractions = list()
        self._analyzors = list()
        self._publishers = list()
        self._populate_analyzors()
        self._populate_dark_subtractions()
        self._populate_publishers()

    def _populate_dark_subtractions(self) -> None:
        config = self._config
        for field in config.image_fields:
            self._dark_subtractions.append(
                DarkSubtraction(field)
            )
        return

    def _populate_analyzors(self) -> None:
        config = self._config
        for image, detector in zip(config.image_fields, config.detectors):
            datakeys = DataKeys(detector, image)
            self._analyzors.append(
                Analyzer(datakeys, config)
            )
        return

    def _populate_publishers(self) -> None:
        config = self._config
        self._publishers.append(
            Publisher(config.address, prefix=config.prefix)
        )
        return

    def __call__(self, name: str, doc: dict) -> DocumentPair:
        for dark_subtraction in self._dark_subtractions:
            name, doc = dark_subtraction(name, doc)
        for analyzer in self._analyzors:
            name, doc = analyzer(name, doc)
        copied_doc = dict(doc)
        for publisher in self._publishers:
            publisher(name, copied_doc)
        return name, doc
