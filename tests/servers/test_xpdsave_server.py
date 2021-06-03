from pkg_resources import resource_filename

import pdfstream.servers.xpdsave_server as mod

fn = resource_filename("tests", "configs/xpdvis_server.ini")


def test_make_and_run():
    mod.make_and_run(fn, test_mode=True)
