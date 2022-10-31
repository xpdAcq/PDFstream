import typing as T
from pathlib import Path

import event_model
import numpy as np
from pdfstream.io import server_message
from tifffile import TiffWriter

from .serializerbase import SerializerBase


class TiffSerializer(SerializerBase):

    def __init__(self, fields: T.List[str], dtype: str, stream_name: str = "primary", folder: str = "dark_sub") -> None:
        super().__init__(folder)
        self._fields = fields
        self._dtype = dtype
        self._stream_name = stream_name
        self._descriptor = ""

    def _get_filepath(self, filename: str, field: str) -> Path:
        f = filename + "_" + field
        filepath = self._directory.joinpath(f).with_suffix(".tiff")
        return filepath

    def _export(self, doc: dict, field: str) -> None:
        image: np.ndarray = doc["data"][field].astype(self._dtype)
        filepath = self._get_filepath(doc["data"]["filename"], field)
        with TiffWriter(str(filepath)) as tf:
            tf.save(image)
        server_message("Save '{}' in '{}'.".format(field, filepath.name))
        return

    def descriptor(self, doc):
        if doc["name"] == self._stream_name:
            self._descriptor = doc['uid']
        return doc

    def event(self, doc):
        if doc["descriptor"] == self._descriptor:
            for field in self._fields:
                if field in doc["data"]:
                    self._export(doc, field)
        return doc
