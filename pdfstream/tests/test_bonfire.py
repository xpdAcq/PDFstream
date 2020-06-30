import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt


def test_average(db):
    with TemporaryDirectory() as temp:
        out_file = Path(temp).joinpath('temp.tiff')
        cp = subprocess.run(
            ['average', out_file, "['{}','{}']".format(db['white_img_file'], db['white_img_file'])],
            cwd=temp
        )
        assert cp.returncode == 0


def test_integrate(db):
    with TemporaryDirectory() as temp:
        cp = subprocess.run(
            ['integrate', db['Ni_poni_file'], db['Ni_img_file'], '--bg_img_file', db['Kapton_img_file'],
             '--bg_scale', '0.04'], cwd=temp
        )
        assert cp.returncode == 0
    plt.close()


def test_instrucalib(db):
    with TemporaryDirectory() as temp:
        cp = subprocess.run(
            ['instrucalib', db['Ni_poni_file'], db['Ni_img_file'], '--fit_range', '(2., 10., .1)'], cwd=temp
        )
        assert cp.returncode == 0
