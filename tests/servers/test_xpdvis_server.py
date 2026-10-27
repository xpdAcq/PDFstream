from importlib.resources import files

import pdfstream.servers.xpdvis_server as mod

fn = str(files("tests").joinpath("configs/xpdvis_server.ini"))


def test_make_and_run():
    mod.make_and_run(fn, test_mode=True)
