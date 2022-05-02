import typing as T
from pathlib import Path

import numpy as np
import event_model
from tifffile import TiffWriter


class TiffSerializer(event_model.DocumentRouter):

    def __init__(self, fields: T.List[str], directory: str, dtype: str = "uint32", stream_name: str = "primary") -> None:
        super().__init__()
        self._fields = fields
        self._dtype = dtype
        self._stream_name = stream_name
        self._directory = Path(directory)
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
        return

    def start(self, doc):
        self._directory.mkdir(exist_ok=True, parents=True)
        return doc

    def descriptor(self, doc):
        if doc["name"] == self._stream_name:
            self._descriptor = doc['uid']
        return doc

    def event(self, doc):
        if doc["descriptor"] == self._descriptor:
            event_model.verify_filled(doc)
            for field in self._fields:
                if field in doc["data"]:
                    self._export(doc, field)
        return doc
