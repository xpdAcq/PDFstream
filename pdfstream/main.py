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

if PDFGETX_AVAILABLE:
    import pdfstream.transformation.cli

    COMMANDS.update({'transform': pdfstream.transformation.cli.transform})


def main():
    """The CLI entry point. Run google-fire on the name - function mapping."""
    fire.Fire(COMMANDS)


if __name__ == "__main__":
    main()
