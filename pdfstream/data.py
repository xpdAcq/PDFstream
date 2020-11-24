"""The paths of data files."""
from pathlib import Path

from pkg_resources import resource_filename

ni_dspacing_file = Path(resource_filename("pdfstream", "data/Ni_dspacing.txt"))
