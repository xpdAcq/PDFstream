import databroker
import typing as tp
from configparser import ConfigParser
from databroker.v2 import Broker
from event_model import RunRouter
from pathlib import Path
from suitcase.csv import Serializer as CSVSerializer
from suitcase.json_metadata import Serializer as JsonSerializer
from suitcase.tiff_series import Serializer as TiffSerializer


class ExportConfig(ConfigParser):
    """The configuration of exporter."""

    @property
    def an_db(self):
        section = self["ANALYSIS DATABASE"]
        name = section.get("name")
        if name:
            return databroker.catalog[name]
        return None

    @property
    def tiff_base(self):
        section = self["FILE SYSTEM"]
        path = Path(section.get("tiff_base"))
        path.mkdir(exist_ok=True)
        return path

    @property
    def run_template(self):
        return self.get("DIR SETTING", "template")

    @property
    def tiff_setting(self):
        section = self["TIFF SETTING"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"file_prefix": section.get("file_prefix")}

    @property
    def json_setting(self):
        section = self["JSON SETTING"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"file_prefix": section.get("file_prefix")}

    @property
    def csv_setting(self):
        section = self["CSV SETTING"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"file_prefix": section.get("file_prefix")}


class Exporter(RunRouter):
    """Export the processed data to file systems, including."""

    def __init__(self, config: ExportConfig, *, test_db: Broker = None):
        factory = ExporterFactory(config, test_db=test_db)
        super().__init__([factory])


class ExporterFactory:
    """The factory for the exporter run router."""

    def __init__(self, config: ExportConfig, *, test_db: Broker = None):
        self.config = config
        self.an_db = self.config.an_db if test_db is None else test_db

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name != "start":
            return [], []
        dir_name = self.config.run_template.format(start=doc)
        base_dir = self.config.tiff_base.joinpath(dir_name)
        cb_lst = []
        if self.an_db is not None:
            cb_lst.append(self.an_db.v1.insert)
        if self.config.tiff_setting is not None:
            cb = TiffSerializer(
                str(base_dir.joinpath("images")),
                **self.config.tiff_setting
            )
            cb_lst.append(cb)
        if self.config.json_setting is not None:
            cb = JsonSerializer(
                str(base_dir.joinpath("metadata")),
                **self.config.json_setting
            )
            cb_lst.append(cb)
        if self.config.csv_setting is not None:
            cb = CSVSerializer(
                str(base_dir.joinpath("datasheets")),
                **self.config.csv_setting
            )
            cb_lst.append(cb)
        return cb_lst, []
