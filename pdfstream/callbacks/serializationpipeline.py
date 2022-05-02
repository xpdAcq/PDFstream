from pathlib import Path

import event_model
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.csvserializer import CSVSerializer
from pdfstream.callbacks.numpyserializer import NumpySerializer
from pdfstream.callbacks.tiffserilaizer import TiffSerializer
from pdfstream.callbacks.yamlserializer import YamlSerializer
import pdfstream.io as io


class SerializationPipeline:

    def __init__(self, config: Config):
        self._config = config
        self._tiff_serilizer = None
        self._csv_serializer = None
        self._numpy_serializer = None
        self._yaml_serializer = None

    def _create(self, doc: dict):
        directory = Path(doc["directory"])
        tiff_dir = directory.joinpath("dark_sub")
        csv_dir = directory.joinpath("scalar_data")
        mask_dir = directory.joinpath("mask")
        yaml_dir = directory.joinpath("meta")
        dkss = self._config.datakeys_list
        image_dtype = self._config.image_dtype
        images = [dks.image for dks in dkss]
        masks = [dks.mask for dks in dkss]
        self._tiff_serilizer = TiffSerializer(images, str(tiff_dir), dtype=image_dtype)
        self._csv_serializer = CSVSerializer(str(csv_dir))
        self._numpy_serializer = NumpySerializer(masks, str(mask_dir))
        self._yaml_serializer = YamlSerializer(str(yaml_dir))
        return

    def __call__(self, name, doc):
        io.server_message("Received the {}.".format(name))
        if str(name) == "start":
            self._create(doc)
        self._tiff_serilizer(name, doc)
        self._csv_serializer(name, doc)
        self._numpy_serializer(name, doc)
        self._yaml_serializer(name, doc)
        return name, doc
    