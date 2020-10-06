from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

import pdfstream.transformation.cli as cli


@pytest.mark.parametrize(
    "parallel",
    [True, False]
)
def test_transform(db, parallel):
    with TemporaryDirectory() as temp_dir:
        dcts = cli.transform(
            db["Ni_gr_file"], db["Ni_chi_file"], output_dir=temp_dir, parallel=parallel, test=True
        )
        for dct in dcts:
            for output_file in dct.values():
                assert Path(output_file).is_file()
