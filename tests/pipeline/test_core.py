from pkg_resources import resource_filename

import pdfstream.pipeline.core as mod

fn = resource_filename("tests", "configs/xpd.ini")


def test_XPDRouter(run0, tmpdir):
    config = mod.XPDConfig()
    config.read(fn)
    config.tiff_base = str(tmpdir)
    cb = mod.XPDRouter(config)
    for name, doc in run0.canonical(fill="yes", strict_order=True):
        cb(name, doc)
    assert len(tmpdir.listdir()) == 1
    folders = tmpdir.listdir()[0].listdir()  # metadata, datasheets, images
    assert len(folders) == 3
    for folder in folders:
        assert len(folder.listdir()) > 0
