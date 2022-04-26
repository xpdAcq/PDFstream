from pdfstream.callbacks.config import Config, ConfigError
from pathlib import Path
import typing as T
from pdfstream.callbacks.ananlysisserver import AnalysisServer
from pdfstream.callbacks.visualizationserver import VisualizationServer
from pdfstream.callbacks.serializationserver import SerializationServer

import fire

try:
    import diffpy.pdfgetx
    PDFGETX_AVAILABLE = True
    del diffpy.pdfgetx
except ImportError:
    PDFGETX_AVAILABLE = False
    print("Warning: diffpy.pdfgetx is not installed. Some functions may raise errors.")

CONFIG_DIR = str(Path("~/.config/pdfstream/").expanduser())


def main():
    """The CLI entry point. Run google-fire on the name - function mapping."""
    import pdfstream.cli as cli
    COMMANDS = {
        'average': cli.average,
        'integrate': cli.integrate,
        'waterfall': cli.waterfall,
        'visualize': cli.visualize
    }
    if PDFGETX_AVAILABLE:
        import pdfstream.transformation.cli
        COMMANDS.update({'transform': pdfstream.transformation.cli.transform})
    fire.Fire(COMMANDS)
    return


def _make_server(cfg_file: str) -> T.Any:
    cfg_path = Path(cfg_file)
    if not cfg_path.is_file():
        cfg_file = find_cfg_file(CONFIG_DIR, cfg_file)
    config = Config()
    config.read_a_file(cfg_file)
    SERVERS = {
        "xpd": AnalysisServer,
        "xpdvis": VisualizationServer,
        "xpdsave": SerializationServer
    }
    if config.server_name not in SERVERS:
        raise ConfigError("No server called '{}'.".format(config.server_name))
    server = SERVERS[config.server_name](config)
    return server


def _run_server(cfg_file: str) -> None:
    """Start a server.

    What server to start depends on the 'name' option in the 'BASICS' section. The allowed options
    are xpd, xpdsave and xpdvis.
    """
    server = _make_server(cfg_file)
    server.start()
    return


def run_server():
    """The CLI entry point."""
    fire.Fire(_run_server)


def print_server_config_dir():
    """The CLI entry point. Print the configuration directory for servers."""
    fire.Fire(lambda: print(str(CONFIG_DIR)))


def find_cfg_file(directory: str, name: str) -> str:
    """Find the configuration file by matching the value of BASIC section name paramter to the name variable."""
    filepath = Path(directory).joinpath(name).with_suffix(".ini")
    if not filepath.is_file():
        raise FileNotFoundError("No such file: {}".format(str(filepath)))
    return str(filepath)
