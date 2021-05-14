import fire


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


def run_server():
    """The CLI entry point. Run the server."""
    try:
        import diffpy.pdfgetx
        del diffpy.pdfgetx
    except ImportError:
        print("Warning: diffpy.pdfgetx is not installed. Some functionalities may not be available.")
    from pdfstream.servers import ServerNames
    import pdfstream.servers.xpd_server as xpd_server
    import pdfstream.servers.lsq_server as lsq_server
    import pdfstream.servers.xpdvis_server as xpdvis_server
    SERVERS = {}
    SERVERS.update({ServerNames.xpd: xpd_server.make_and_run})
    SERVERS.update({ServerNames.lsq: lsq_server.make_and_run})
    SERVERS.update({ServerNames.xpdvis: xpdvis_server.make_and_run})
    fire.Fire(SERVERS)


def print_server_config_dir():
    """The CLI entry point. Print the configuration directory for servers."""
    from pdfstream.servers import CONFIG_DIR
    fire.Fire(lambda: print(str(CONFIG_DIR)))
