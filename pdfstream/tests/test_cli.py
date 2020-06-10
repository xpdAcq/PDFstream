from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pytest

import pdfstream.cli as cli
import pdfstream.io as io


@pytest.mark.parametrize(
    'kwargs', [
        {'bg_img_file': None},
        {'mask_setting': {'alpha': 1.}},
        {'integ_setting': {'npt': 1024}},
        {'plot_setting': {'ls': '--'}},
        {'img_setting': {'vmin': 0}}
    ]
)
def test_integrate(db, kwargs):
    with TemporaryDirectory() as tempdir:
        img_file = Path(db['white_img_file'])
        chi_file = Path(tempdir).joinpath(img_file.with_suffix('.chi').name)
        _kwargs = {'bg_img_file': db['black_img_file'], 'output_dir': tempdir}
        _kwargs.update(kwargs)
        cli.integrate(db['Ni_poni_file'], str(img_file), **_kwargs)
        assert chi_file.exists()


@pytest.mark.parametrize(
    'kwargs', [
        {},
        {'weights': [1, 1]}
    ]
)
def test_average(db, kwargs):
    with TemporaryDirectory() as tempdir:
        img_file = Path(tempdir).joinpath('average.tiff')
        cli.average(img_file, [db['white_img_file'], db['white_img_file']], **kwargs)
        avg_img = io.load_img(img_file)
        white_img = io.load_img(db['white_img_file'])
        assert np.array_equal(avg_img, white_img)
