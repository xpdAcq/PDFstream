from pathlib import Path

import pdfstream.io as io
import yaml
from bluesky.callbacks.core import CallbackBase


class YamlSerializer(CallbackBase):
    """Export the start document in yaml file."""

    def __init__(self, directory: str) -> None:
        super().__init__()
        self._directory = Path(directory)

    def _get_filepath(self, doc: dict) -> Path:
        return self._directory.joinpath(doc["filename"]).with_suffix(".yml")

    def start(self, doc):
        self._directory.mkdir(exist_ok=True, parents=True)
        file_path = self._get_filepath(doc)
        with file_path.open("w") as f:
            yaml.safe_dump(doc, f)
        io.server_message("Save start document of '{}'.".format(doc["uid"]))
        return doc
