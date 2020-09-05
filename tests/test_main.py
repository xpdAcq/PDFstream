import subprocess
from pathlib import Path

from pkg_resources import resource_filename


def test_cli_main():
    main_file = Path(resource_filename('pdfstream', 'main.py'))
    cp = subprocess.run(['$PYTHON', str(main_file), '--', '--help'], shell=True)
    assert cp.returncode == 0
