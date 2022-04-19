import datetime
import typing as T

import pdfstream.io as io
from bluesky.callbacks import CallbackBase
from pdfstream.vend.formatters import SpecialStr


class FileNameRender(CallbackBase):

    def __init__(self, file_prefix: str, hints: T.List[str] = None) -> None:
        super().__init__()
        self._file_template = SpecialStr(file_prefix)
        self._force_hints = hints if hints else list()
        self._hints = list()
        self._units = list()
        self._file_prefix = ""
        self._file_name = ""

    def _set_file_prefix(self, doc: dict) -> None:
        self._file_prefix = self._file_template.format(**doc)
        io.server_message("Render file prefix.")
        return

    def start(self, doc: dict) -> None:
        self._set_file_prefix(doc)
        return

    def _set_hints(self, doc: dict) -> None:
        if self._force_hints:
            self._hints = self._force_hints.copy()
            io.server_message("Use provided hints '{}'.".format(self._hints))
            return
        hints = []
        dims = doc.get("hints", {}).get("dimensions", [])
        for data_keys, stream_name in dims:
            if stream_name == "primary":
                hints.extend(data_keys)
        self._hints = hints
        io.server_message("The hints are '{}'.".format(hints))
        return

    def _set_units(self, doc: dict) -> None:
        data_keys = doc.get("data_keys", {})
        self._units = [
            data_keys.get(k, {}).get("units", "")
            for k in self._hints
        ]
        io.server_message("The units of the hints are obtained.")
        return

    def _get_timestamp(self, doc: dict) -> str:
        return datetime.datetime.fromtimestamp(
            doc["time"]
        ).strftime(
            "%Y%m%d-%H%M%S"
        )

    def _get_hints_str(self, doc: dict) -> str:
        hints = self._hints
        units = self._units
        data = doc["data"]
        stack = []
        for hint, unit in zip(hints, units):
            if hint in data:
                value = data[hint]
                if isinstance(value, float):
                    s = "{}_{:.2f}{}".format(hint, value, unit).replace(".", ",")
                elif isinstance(value, int):
                    s = "{}_{}{}".format(hint, value, unit)
                else:
                    s = "{}_{}".format(hint, value)
                stack.append(s)
        return '_'.join(stack)

    def _get_numstamp(self, doc: dict) -> str:
        return "{:04d}".format(doc["seq_num"])

    def _get_rendered_middle(self, doc: dict) -> str:
        t = self._get_timestamp(doc)
        h = self._get_hints_str(doc)
        n = self._get_numstamp(doc)
        items = [t, h, n] if h else [t, n]
        return '_'.join(items) + "_"

    def _set_filename(self, doc: dict) -> None:
        p = self._file_prefix
        m = self._get_rendered_middle(doc)
        filename = p + m
        self._file_name = filename
        io.server_message("The filename will be '{}'.".format(filename))
        return

    def event(self, doc):
        self._set_filename(doc)
        return

    @property
    def filename(self) -> str:
        return self._file_name
