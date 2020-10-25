import fire

import pdfstream.cli as cli

try:
    import diffpy.pdfgetx

    PDFGETX_AVAILABLE = True
    del diffpy.pdfgetx
except ImportError:
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
    import pdfstream.servers.xpd_server as xpd_server

    COMMANDS.update({'transform': pdfstream.transformation.cli.transform})
    SERVERS.update({'xpd': xpd_server.make_and_run})


def main():
    """The CLI entry point. Run google-fire on the name - function mapping."""
    fire.Fire(COMMANDS)


def server_start():
    fire.Fire(SERVERS)


if __name__ == "__main__":
    main()
