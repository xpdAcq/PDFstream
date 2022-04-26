from pathlib import Path

from pdfstream.callbacks.config import Config
from pdfstream.main import _make_server
from pkg_resources import resource_filename

CONFIG_FILE = Path(resource_filename("pdfstream", "data/config_files/simulation.ini"))


def test_write_config(local_dir: Path):
    config_file = local_dir.joinpath("config.ini")
    config = Config()
    with config_file.open("w") as f:
        config.write(f)
    return
