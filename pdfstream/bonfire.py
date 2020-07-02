"""The cli interface that uses the fire to fire the functions in the cli."""
import fire

import pdfstream.cli as cli


def pdf_integrate():
    """The CLI of 'integrate'."""
    fire.Fire(cli.integrate)
    return


def pdf_average():
    """The CLI of 'average'."""
    fire.Fire(cli.average)
    return


def pdf_instrucalib():
    """The CLI of 'intrucalib'."""
    fire.Fire(cli.instrucalib)
    return
