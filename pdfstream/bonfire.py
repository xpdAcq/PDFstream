"""The cli interface that uses the fire to fire the functions in the cli."""
import fire

import pdfstream.cli as cli


def integrate():
    """The CLI to integrate images."""
    fire.Fire(cli.integrate)
    return


def average():
    """The CLI to average images."""
    fire.Fire(cli.average)
    return
