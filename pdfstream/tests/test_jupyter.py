from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
from pyperclip import PyperclipException

from pdfstream.utils.jupyter import savefig_factory


def test_savefig_factory():
    plt.figure()
    with TemporaryDirectory() as d:
        savefig = savefig_factory(figure_dir=d)
        fname = 'test.png'
        path = Path(d).joinpath(fname)
        try:
            savefig(str(path))
            assert path.exists()
        except PyperclipException:
            print("No mechanism for clipping.")
    plt.close()
