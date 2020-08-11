import subprocess


def test_cli_main():
    cp = subprocess.run(['pdfstream', '--', '--help'])
    assert cp.returncode == 0
