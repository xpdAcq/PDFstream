import time
import typing as T
from multiprocessing import Process
from pathlib import Path

import fire

import pdfstream.callbacks.ananlysisserver as analysis
import pdfstream.callbacks.serializationserver as serialization
import pdfstream.callbacks.visualizationserver as visualization

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
        "average": cli.average,
        "integrate": cli.integrate,
        "waterfall": cli.waterfall,
        "visualize": cli.visualize,
    }
    if PDFGETX_AVAILABLE:
        import pdfstream.transformation.cli

        COMMANDS.update({"transform": pdfstream.transformation.cli.transform})
    fire.Fire(COMMANDS)
    return


def _run_processes(ps: T.List[Process], rate: float = 0.5) -> None:
    for p in ps:
        p.start()
    try:
        while True:
            time.sleep(rate)
    except KeyboardInterrupt:
        for p in ps:
            p.kill()
        for p in ps:
            p.join()
    return


def _run_server(cfg_file: str) -> None:
    """Start a server.

    What server to start depends on the 'name' option in the 'BASICS' section. The allowed options
    are xpd, xpdsave and xpdvis.
    """
    cfg_path = Path(cfg_file)
    if not cfg_path.is_file():
        cfg_file = find_cfg_file(CONFIG_DIR, cfg_file)
    ps = [
        analysis.get_process(str(cfg_file)),
        serialization.get_process(str(cfg_file)),
        visualization.get_process(str(cfg_file)),
    ]
    _run_processes(ps)
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
