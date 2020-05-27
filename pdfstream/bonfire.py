"""The cli interface that uses the fire to fire the functions in the cli."""
import fire

import pdfstream.cli as cli


def integrate():
    """The CLI of image_to_iq."""
    fire.Fire(cli.integrate)
    return
