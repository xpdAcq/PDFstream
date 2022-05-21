import typing as T
from pathlib import Path

from event_model import DocumentRouter
from matplotlib.figure import Figure


class PlotterBaseError(Exception):

    pass


class PlotterBase(DocumentRouter):

    def __init__(self, name: str, figure: Figure, folder: str = "plots", stream_name: str = "primary", save_at_stop: bool = False, save_at_event: bool = False, suffix: str = ".png"):
        super().__init__()
        self._name = name
        self._figure = figure
        self._suffix = suffix
        self._folder = folder
        self._stream_name = stream_name
        self._save_at_stop = save_at_stop
        self._save_at_event = save_at_event
        self._filename = None
        self._directory = None
        self._descriptor = ""
        self._updated = False

    def mkdir(self, doc) -> None:
        if "directory" not in doc:
            raise PlotterBaseError("Missing key 'directory' in the doc.")
        self._directory = Path(doc["directory"]).joinpath(self._folder)
        self._directory.mkdir(exist_ok=True, parents=True)
        return

    def set_filename(self, doc) -> None:
        if "filename" not in doc:
            raise PlotterBaseError("No 'filename' in start.")
        self._filename = doc["filename"]
        return

    def save_figure(self) -> None:
        f = self._filename + "_" + self._name + self._suffix
        fpath = self._directory.joinpath(f)
        self._figure.savefig(fpath)
        return

    def plot_event(self, doc) -> T.Any:
        return NotImplemented

    def start(self, doc):
        self._updated = False
        if self._save_at_stop or self._save_at_event:
            self.mkdir(doc)
        if self._save_at_stop:
            self.set_filename(doc)
        return doc

    def descriptor(self, doc):
        if doc["name"] == self._stream_name:
            self._descriptor = doc["uid"]
        return doc

    def event(self, doc):
        if doc["descriptor"] == self._descriptor:
            self.plot_event(doc)
            self._figure.canvas.draw_idle()
            if int(doc['seq_num']) == 1:
                self._figure.show()
            if self._save_at_event and self._updated:
                self.set_filename(doc["data"])
                self.save_figure()
        return doc

    def stop(self, doc):
        if self._save_at_stop and self._updated:
            self.save_figure()
        return doc
