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
    def db(self):
        section = self["ANALYSIS DATABASE"]
        if section.getboolean("test", fallback=False):
            return databroker.v2.temp()
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
        return {
            "template": section.get("template"),
            "enable": section.getboolean("enable", fallback=True)
        }

    @property
    def json_setting(self):
        section = self["JSON SETTING"]
        return {
            "template": section.get("template"),
            "enable": section.getboolean("enable", fallback=True)
        }

    @property
    def csv_setting(self):
        section = self["CSV SETTING"]
        return {
            "template": section.get("template"),
            "enable": section.getboolean("enable", fallback=True)
        }


class Exporter(RunRouter):
    """Export the processed data to file systems, including."""

    def __init__(self, config: ExportConfig):
        factory = ExporterFactory(config)
        super().__init__([factory])


class DBDumper:
    """Dump the data into analysis database."""
    pass


class ExporterFactory:
    """The factory for the exporter run router."""

    def __init__(self, config: ExportConfig):
        self.config = config

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name != "start":
            return [], []
        dir_name = self.config.run_template.format(start=doc)
        base_dir = self.config.tiff_base.joinpath(dir_name)
        cb_lst = []
        if self.config.tiff_setting["enable"]:
            cb = TiffSerializer(
                str(base_dir.joinpath("images")),
                file_prefix=self.config.tiff_setting["template"]
            )
            cb_lst.append(cb)
        if self.config.json_setting["enable"]:
            cb = JsonSerializer(
                str(base_dir.joinpath("metadata")),
                file_prefix=self.config.json_setting["template"]
            )
            cb_lst.append(cb)
        if self.config.csv_setting["enable"]:
            cb = CSVSerializer(
                str(base_dir.joinpath("datasheets")),
                file_prefix=self.config.csv_setting["template"]
            )
            cb_lst.append(cb)
        return cb_lst, []
