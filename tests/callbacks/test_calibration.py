from pkg_resources import resource_filename

import pdfstream.callbacks.calibration as mod

fn = resource_filename("tests", "configs/xpd_server.ini")


def test_Calibration(db_with_dark_and_calib, tmpdir):
    db = db_with_dark_and_calib
    config = mod.CalibrationConfig()
    config.read(fn)
    config.tiff_base = str(tmpdir)
    config.calib_base = str(tmpdir)
    cb = mod.Calibration(config, test=True)
    for name, doc in db[-1].canonical(fill="yes"):
        cb(name, doc)
    assert len(list(config.tiff_base.joinpath("calib").rglob("*.tiff"))) > 0
