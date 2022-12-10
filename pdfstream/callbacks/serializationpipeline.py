from pdfstream.callbacks.config import Config
from pdfstream.callbacks.csvserializer import CSVSerializer
from pdfstream.callbacks.numpyserializer import NumpySerializer
from pdfstream.callbacks.tiffserilaizer import TiffSerializer
from pdfstream.callbacks.yamlserializer import YamlSerializer


class SerializationPipeline:
    def __init__(self, config: Config):
        tiff_base = config.tiff_base
        dkss = config.datakeys_list
        image_dtype = config.image_dtype
        images = [dks.image for dks in dkss]
        masks = [dks.mask for dks in dkss]
        self._config = config
        self._yaml_serializers = [YamlSerializer(d) for d in tiff_base]
        self._csv_serializers = [CSVSerializer(d) for d in tiff_base]
        self._tiff_serilizers = [
            TiffSerializer(d, images, image_dtype) for d in tiff_base
        ]
        self._numpy_serializers = [NumpySerializer(d, masks) for d in tiff_base]
        return

    def __call__(self, name, doc):
        for s in self._yaml_serializers:
            s(name, doc)
        for s in self._csv_serializers:
            s(name, doc)
        for s in self._tiff_serilizers:
            s(name, doc)
        for s in self._numpy_serializers:
            s(name, doc)
        return name, doc
