from pkg_resources import resource_filename

import pdfstream.pipeline.core as mod

fn = resource_filename("tests", "configs/xpd.ini")


def test_XPDRouter(run0):
    config = mod.XPDConfig()
    config.read(fn)
    cb = mod.XPDRouter(config)
    for name, doc in run0.canonical(fill="yes", strict_order=True):
        cb(name, doc)
