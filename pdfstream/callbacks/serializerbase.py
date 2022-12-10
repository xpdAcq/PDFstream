from pathlib import Path

from event_model import DocumentRouter


class SerializerBaseError(Exception):

    pass


class SerializerBase(DocumentRouter):
    def __init__(self, base: str, folder: str):
        super().__init__()
        self._base = base
        self._folder = folder
        self._directory = None

    def mkdir(self, doc: dict) -> None:
        self.setdir(doc)
        self._directory.mkdir(exist_ok=True)
        return

    def setdir(self, doc: dict) -> None:
        if "directory" not in doc:
            raise SerializerBaseError("Missing key 'directory' in the doc.")
        self._directory = Path(self._base, doc["directory"], self._folder)
        return

    def start(self, doc):
        self.mkdir(doc)
        return doc
