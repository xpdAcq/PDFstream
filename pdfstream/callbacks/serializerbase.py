from pathlib import Path

from event_model import DocumentRouter


class SerializerBaseError(Exception):

    pass


class SerializerBase(DocumentRouter):

    def __init__(self, folder: str):
        super().__init__()
        self._folder = folder
        self._directory = None

    def mkdir(self, doc) -> None:
        if "directory" not in doc:
            raise SerializerBaseError("Missing key 'directory' in the doc.")
        self._directory = Path(doc["directory"]).joinpath(self._folder)
        self._directory.mkdir(exist_ok=True, parents=True)
        return

    def start(self, doc):
        self.mkdir(doc)
        return doc
