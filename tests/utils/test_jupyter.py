from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt

from pdfstream.utils.jupyter import savefig_factory


def test_savefig_factory():
    plt.figure()
    with TemporaryDirectory() as d:
        figure_forlder = Path(d) / "figures"
        savefig = savefig_factory(figure_dir=figure_forlder)
        fname = 'test.png'
        savefig(fname)
        figure_path = figure_forlder / fname
        assert figure_path.exists()
    plt.close()
