from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt

from pdfstream.utils.jupyter import savefig_factory, FigExporter


def test_savefig_factory():
    plt.figure()
    with TemporaryDirectory() as d:
        figure_forlder = Path(d) / "figures"
        savefig = savefig_factory(figure_dir=figure_forlder)
        fname = 'test.png'
        savefig(fname)
        figure_path = figure_forlder / fname
        assert figure_path.exists()
    plt.clf()


def test_FigExporter():
    plt.figure()
    with TemporaryDirectory() as d:
        figure_dir = Path(d) / "test"
        exporter = FigExporter(str(figure_dir))
        exporter.update(dpi=40)
        exporter("test.svg")
        exporter.latex()
        target = figure_dir / "test.svg"
        assert target.is_file()
    plt.clf()
