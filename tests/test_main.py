import subprocess
from pkg_resources import resource_filename
from pathlib import Path


def test_cli_main():
    main_file = Path(resource_filename('pdfstream', 'main.py'))
    cp = subprocess.run(['$PYTHON', str(main_file), '--', '--help'], shell=True)
    assert cp.returncode == 0
