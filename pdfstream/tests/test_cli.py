from pathlib import Path
from tempfile import TemporaryDirectory

import pdfstream.cli as cli


def test_integrate(db):
    with TemporaryDirectory() as tempdir:
        chi_file = Path(tempdir).joinpath('Ni_img_file.chi')
        cli.integrate(db['Ni_img_file'], db['Ni_poni_file'], bg_img_file=db['Kapton_img_file'],
                      output_dir=tempdir)
        assert chi_file.exists()
