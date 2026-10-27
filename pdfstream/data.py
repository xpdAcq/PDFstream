"""The paths of data files and other package variables."""
from importlib.resources import files

ni_dspacing_file = files("pdfstream").joinpath("data/Ni_dspacing.txt")
QUIET = False
