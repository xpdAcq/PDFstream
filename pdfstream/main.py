import typing as T
from pathlib import Path
import multiprocessing, logging
from multiprocessing import Process
import time

import fire

from pdfstream.callbacks.ananlysisserver import AnalysisServer
from pdfstream.callbacks.config import Config, ConfigError
from pdfstream.callbacks.serializationserver import SerializationServer
from pdfstream.callbacks.visualizationserver import VisualizationServer

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


def create_logger(log_file: str):
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(\
        '[%(asctime)s| %(levelname)s| %(processName)s] %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    # this bit will make sure you won't have 
    # duplicated messages in the output
    if not len(logger.handlers): 
        logger.addHandler(handler)
    return logger


def _start_server(server: T.Any, cfg_file: str) -> None:
    config = Config()
    config.read_a_file(cfg_file)
    return server(config).start()


def _run_server(cfg_file: str) -> None:
    """Start a server.

    What server to start depends on the 'name' option in the 'BASICS' section. The allowed options
    are xpd, xpdsave and xpdvis.
    """
    cfg_path = Path(cfg_file)
    if not cfg_path.is_file():
        cfg_file = find_cfg_file(CONFIG_DIR, cfg_file)
    config = Config()
    config.read_a_file(cfg_file)
    create_logger(str(config.log_file))
    servers = (AnalysisServer, SerializationServer, VisualizationServer)
    processes = []
    for server in servers:
        p = Process(
            target=_start_server, 
            args=(server, cfg_file), 
            name="pdfstream"
        )
        processes.append(p)
    for p in processes:
        p.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        for p in processes:
            p.kill()
            p.join()
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
