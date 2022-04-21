from pathlib import Path

from bluesky.callbacks.core import CallbackBase
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.csvserializer import CSVSerializer
from pdfstream.callbacks.numpyserializer import NumpySerializer
from pdfstream.callbacks.tiffserilaizer import TiffSerializer


class SerializationPipeline(CallbackBase):

    def __init__(self, config: Config):
        super().__init__()
        self._config = config
        self._tiff_serilizer = None
        self._csv_serializer = None
        self._numpy_serializer = None

    def _create(self, doc: dict):
        directory = Path(doc["directory"])
        directory.mkdir(exist_ok=True, parents=True)
        dkss = self._config.datakeys_list
        images = [dks.image for dks in dkss]
        masks = [dks.mask for dks in dkss]
        self._tiff_serilizer = TiffSerializer(images, str(directory))
        self._csv_serializer = CSVSerializer(str(directory))
        self._numpy_serializer = NumpySerializer(masks, str(directory))

    def __call__(self, name, doc):
        if name == "start":
            self._create(doc)
        self._tiff_serilizer(name, doc)
        self._csv_serializer(name, doc)
        self._numpy_serializer(name, doc)
        return name, doc
    