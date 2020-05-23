from pathlib import Path
from tempfile import TemporaryDirectory

import pdfstream.cli as cli


def test_image_to_iq(db):
    with TemporaryDirectory() as tempdir:
        chi_file = Path(tempdir).joinpath('Ni_img_file.chi')
        cli.image_to_iq(db['Ni_img_file'], db['Ni_poni_file'], bg_img_file=db['Kapton_img_file'],
                        output_dir=tempdir, bg_scale=0)
        assert chi_file.exists()
