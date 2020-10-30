from pathlib import Path

from pkg_resources import resource_filename

import pdfstream.pipeline.core as mod

fn = resource_filename("tests", "configs/xpd.ini")


def test_XPDRouter(db_with_dark_and_scan, tmpdir):
    raw_db = db_with_dark_and_scan
    config = mod.XPDConfig()
    config.read(fn)
    config.tiff_base = str(tmpdir)
    config.calib_base = str(tmpdir)
    cb = mod.XPDRouter(config, raw_db=raw_db)
    for name, doc in raw_db[-1].canonical(fill="yes", strict_order=True):
        cb(name, doc)
    tiff_base = Path(config.tiff_base)
    assert len(list(tiff_base.rglob("*.tiff"))) > 0
    assert len(list(tiff_base.rglob("*.csv"))) > 0
    assert len(list(tiff_base.rglob("*.json"))) > 0
