import fire

import pdfstream.cli as cli
from pdfstream.servers import ServerNames, CONFIG_DIR

try:
    import diffpy.pdfgetx

    PDFGETX_AVAILABLE = True
    del diffpy.pdfgetx
except ImportError:
    print("Warning: diffpy.pdfgetx is not installed. Some functionalities may not be available.")
    PDFGETX_AVAILABLE = False

COMMANDS = {
    'average': cli.average,
    'integrate': cli.integrate,
    'waterfall': cli.waterfall,
    'visualize': cli.visualize
}

SERVERS = {}

if PDFGETX_AVAILABLE:
    import pdfstream.transformation.cli

    COMMANDS.update({'transform': pdfstream.transformation.cli.transform})

    import pdfstream.servers.xpd_server as xpd_server
    import pdfstream.servers.lsq_server as lsq_server
    import pdfstream.servers.xpdvis_server as xpdvis_server

    SERVERS.update({ServerNames.xpd: xpd_server.make_and_run})
    SERVERS.update({ServerNames.lsq: lsq_server.make_and_run})
    SERVERS.update({ServerNames.xpdvis: xpdvis_server.make_and_run})


def main():
    """The CLI entry point. Run google-fire on the name - function mapping."""
    fire.Fire(COMMANDS)


def run_server():
    """The CLI entry point. Run the server."""
    fire.Fire(SERVERS)


def print_server_config_dir():
    """The CLI entry point. Print the configuration directory for servers."""
    fire.Fire(lambda: print(str(CONFIG_DIR)))
