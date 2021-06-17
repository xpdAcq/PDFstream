from configparser import ConfigParser
from pathlib import Path

import fire

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
    try:
        import diffpy.pdfgetx
        del diffpy.pdfgetx
        PDFGETX_AVAILABLE = True
    except ImportError:
        print("Warning: diffpy.pdfgetx is not installed. Some functionalities may not be available.")
        PDFGETX_AVAILABLE = False
    if PDFGETX_AVAILABLE:
        import pdfstream.transformation.cli
        COMMANDS.update({'transform': pdfstream.transformation.cli.transform})
    fire.Fire(COMMANDS)


def _run_server(cfg_file: str):
    """Build the server according to the configuration file and run it.

    The servers include:

        xpd server: transer the diffraction image to the pair distribution function.
        xpdvis server: visualize the results from the xpd server.
        xpdsave server: visualize the resluts from the xpdsave server.
        lsq server: decompose the pair distribution function from the xpd server.
    """
    try:
        import diffpy.pdfgetx
        del diffpy.pdfgetx
    except ImportError:
        print("Warning: diffpy.pdfgetx is not installed. Some servers may encounter errors.")
    # read configs
    cfg_path = Path(cfg_file)
    if not cfg_path.is_file():
        cfg_file = find_cfg_file(CONFIG_DIR, cfg_file)
    config = ConfigParser()
    results = config.read(cfg_file)
    if not results:
        raise FileNotFoundError("Not a valid file: {}".format(cfg_file))
    server_type = config["BASIC"]["name"]
    # run the servers
    import pdfstream.servers.xpd_server as xpd_server
    import pdfstream.servers.lsq_server as lsq_server
    import pdfstream.servers.xpdvis_server as xpdvis_server
    import pdfstream.servers.xpdsave_server as xpdsave_server
    SERVERS = {
        "xpd": xpd_server.make_and_run,
        "lsq": lsq_server.make_and_run,
        "xpdvis": xpdvis_server.make_and_run,
        "xpdsave": xpdsave_server.make_and_run
    }
    return SERVERS[server_type](cfg_file)


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
