from pkg_resources import resource_filename

import pdfstream.callbacks.calibration as mod

fn = resource_filename("tests", "configs/xpd_server.ini")


def test_Calibration(db_with_dark_and_calib, tmpdir):
    db = db_with_dark_and_calib
    config = mod.CalibrationConfig()
    config.read(fn)
    config.calib_base = str(tmpdir)
    cb = mod.Calibration(config, test=True)
    for name, doc in db[-1].canonical(fill="yes"):
        cb(name, doc)
    assert len(list(config.calib_base.rglob("*.tiff"))) > 0


def test_Calibration_error(db_with_dark_and_calib, tmpdir):
    """Test error message when wavelength is None."""
    db = db_with_dark_and_calib
    config = mod.CalibrationConfig()
    config.read(fn)
    config.tiff_base = str(tmpdir)
    config.calib_base = str(tmpdir)
    cb = mod.Calibration(config, test=True)
    for name, doc in db[-1].canonical(fill="yes"):
        if name == "start":
            doc = dict(**doc)
            doc.update({"bt_wavelength": None})
        cb(name, doc)
