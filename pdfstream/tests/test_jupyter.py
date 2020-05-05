from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt

from pdfstream.utils.jupyter import savefig_factory


def test_savefig_factory():
    plt.figure()
    with TemporaryDirectory() as d:
        savefig = savefig_factory(figure_dir=d)
        fname = 'test.png'
        path = Path(d).joinpath(fname)
        savefig(fname)
        assert path.exists()
