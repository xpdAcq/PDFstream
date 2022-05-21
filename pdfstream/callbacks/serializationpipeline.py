from pdfstream.callbacks.config import Config
from pdfstream.callbacks.csvserializer import CSVSerializer
from pdfstream.callbacks.numpyserializer import NumpySerializer
from pdfstream.callbacks.tiffserilaizer import TiffSerializer
from pdfstream.callbacks.yamlserializer import YamlSerializer


class SerializationPipeline:

    def __init__(self, config: Config):
        self._config = config
        self._tiff_serilizer = None
        self._csv_serializer = None
        self._numpy_serializer = None
        self._yaml_serializer = None
        dkss = self._config.datakeys_list
        image_dtype = self._config.image_dtype
        images = [dks.image for dks in dkss]
        masks = [dks.mask for dks in dkss]
        self._tiff_serilizer = TiffSerializer(images, image_dtype)
        self._csv_serializer = CSVSerializer()
        self._numpy_serializer = NumpySerializer(masks)
        self._yaml_serializer = YamlSerializer()
        return

    def __call__(self, name, doc):
        self._yaml_serializer(name, doc)
        self._csv_serializer(name, doc)
        self._tiff_serilizer(name, doc)
        self._numpy_serializer(name, doc)
        return name, doc
