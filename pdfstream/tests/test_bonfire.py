import subprocess

import pytest


@pytest.mark.parametrize(
    'args',
    [
        ['integrate', '--', '--help'],
        ['average', '--', '--help'],
        ['instrucalib', '--', '--help']
    ]
)
def test_commands(args):
    subprocess.run(args)
