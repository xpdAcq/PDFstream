from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

import pdfstream.cli as cli
import pdfstream.io as io


def test_integrate(db):
    with TemporaryDirectory() as tempdir:
        chi_file = Path(tempdir).joinpath('Ni_img_file.chi')
        cli.integrate(db['Ni_img_file'], db['Ni_poni_file'], bg_img_file=db['Kapton_img_file'],
                      output_dir=tempdir)
        assert chi_file.exists()


def test_average(db):
    with TemporaryDirectory() as tempdir:
        img_file = Path(tempdir).joinpath('average.tiff')
        cli.average(img_file, [db['white_img_file'], db['white_img_file']], weights=[1, 1])
        avg_img = io.load_img(img_file)
        white_img = io.load_img(db['white_img_file'])
        assert np.array_equal(avg_img, white_img)
