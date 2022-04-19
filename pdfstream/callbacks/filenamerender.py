import datetime

import pdfstream.io as io
from bluesky.callbacks import CallbackBase
from pdfstream.callbacks.config import Config


class FileNameRender(CallbackBase):

    def __init__(self, config: Config) -> None:
        super().__init__()
        self._config = config
        self._uid = ""
        self._hints = list()
        self._units = list()
        self._directory = ""
        self._file_prefix = ""
        self._file_name = ""

    def _set_file_prefix(self, doc: dict) -> None:
        template = self._config.file_prefix
        self._file_prefix = template.format(**doc)
        io.server_message("Render file prefix.")
        return

    def _set_directory(self, doc: dict) -> None:
        template = self._config.directory
        base = self._config.tiff_base
        d = template.format(**doc)
        self._directory = str(base.joinpath(d))
        return

    def _set_uid(self, doc: dict) -> None:
        self._uid = doc["uid"][:6]
        return

    def _get_timestamp(self, doc: dict) -> str:
        return datetime.datetime.fromtimestamp(
            doc["time"]
        ).strftime(
            "%Y%m%d-%H%M%S"
        )

    def _add_data_keys(self, doc: dict) -> None:
        doc["data_keys"]["filename"] = {
            "dtype": "string",
            "shape": [],
            "source": self.__class__.__name__,
        }
        return

    def _set_hints(self, doc: dict) -> None:
        forced_hints = self._config.hints
        if forced_hints:
            self._hints = forced_hints
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
        u = self._uid
        h = self._get_hints_str(doc)
        n = self._get_numstamp(doc)
        items = [t, u, h, n] if h else [t, u, n]
        return '_'.join(items)

    def _set_filename(self, doc: dict) -> None:
        p = self._file_prefix
        m = self._get_rendered_middle(doc)
        filename = p + "_" + m
        self._file_name = filename
        io.server_message("The filename will be '{}'.".format(filename))
        return

    def _add_filename(self, doc: dict) -> None:
        doc["data"]["filename"] = self._file_name
        return

    def start(self, doc):
        self._set_uid(doc)
        self._set_file_prefix(doc)
        self._set_directory(doc)
        t = self._get_timestamp(doc)
        doc["filename"] = self._file_prefix + "_" + t + "_" + self._uid
        doc["directory"] = self._directory
        return doc

    def descriptor(self, doc):
        self._add_data_keys(doc)
        return doc

    def event(self, doc):
        self._set_filename(doc)
        self._add_filename(doc)
        return
