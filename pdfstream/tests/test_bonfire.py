import subprocess

import pytest


@pytest.mark.parametrize(
    'args',
    [
        ['pdf_integrate', '--', '--help'],
        ['pdf_average', '--', '--help'],
        ['pdf_instrucalib', '--', '--help'],
        ['pdf_visualize', '--', '--help'],
        ['pdf_waterfall', '--', '--help']
    ]
)
def test_commands(args):
    cp = subprocess.run(args)
    assert cp.returncode == 0
