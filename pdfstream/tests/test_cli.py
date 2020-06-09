from pathlib import Path
from tempfile import TemporaryDirectory

import pdfstream.cli as cli


def test_integrate(db):
    with TemporaryDirectory() as tempdir:
        chi_file0 = Path(tempdir).joinpath('Ni_img_file.chi')
        cli.integrate(db['Ni_img_file'], db['Ni_poni_file'], bg_img_file=db['Kapton_img_file'], bg_scale= 0.2,
                      output_dir=tempdir)
        assert chi_file0.exists()
    with TemporaryDirectory() as tempdir:
        chi_file1 = Path(tempdir).joinpath('Ni_img_file.chi')
        cli.integrate(db['Ni_img_file'], db['Ni_poni_file'], mask_setting="OFF",
                      output_dir=tempdir)
        assert chi_file1.exists()
