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


def test_make_servers(tmp_path: Path):
    config = Config()
    for server in ("xpd", "xpdsave"):
        config.set("BASIC", "name", server)
        config_file = tmp_path.joinpath("{}.ini".format(server))
        with config_file.open("w") as f:
            config.write(f)
        _make_server(str(config_file))
