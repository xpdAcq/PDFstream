from pathlib import Path

import pdfstream.io as io
import yaml

from .serializerbase import SerializerBase


class YamlSerializer(SerializerBase):
    """Export the start document in yaml file."""

    def __init__(self, base: str, folder: str = "meta") -> None:
        super().__init__(base, folder)

    def _get_filepath(self, doc: dict) -> Path:
        return self._directory.joinpath(doc["filename"]).with_suffix(".yml")

    def start(self, doc):
        super().start(doc)
        file_path = self._get_filepath(doc)
        with file_path.open("w") as f:
            yaml.safe_dump(doc, f)
        io.server_message("Save start document of '{}'.".format(doc["uid"]))
        return doc
