from pathlib import Path

import databroker
import databroker.v2
import pytest
from pkg_resources import resource_filename

import pdfstream.servers.xpd_server as mod

fn = resource_filename("tests", "configs/xpd_server.ini")


def test_XPDServer(tmpdir):
    config = mod.XPDServerConfig()
    config.read(fn)
    config.tiff_base = str(tmpdir)
    config.calib_base = str(tmpdir)
    config.raw_db = databroker.v2.temp()
    config["FUNCTIONALITY"]["send_messages"] = "True"
    mod.XPDServer(config)


@pytest.mark.parametrize(
    "start_doc, expect_lst",
    [
        ({"dark_frame": True}, []),
        ({"is_calibration": True}, [mod.Calibration]),
        ({}, [mod.AnalysisStream])
    ]
)
def test_XPDFactroy(start_doc, expect_lst):
    """Assert XPDFactory output the correct callback function list."""
    config = mod.XPDConfig()
    config.read(fn)
    factory = mod.XPDFactory(config)
    out_lst, _ = factory("start", start_doc)
    _, _ = factory("stop", {})
    for obj, cls in zip(out_lst, expect_lst):
        assert isinstance(obj, cls)


def test_XPDRouter(db_with_img_and_bg_img, tmpdir):
    raw_db = db_with_img_and_bg_img
    config = mod.XPDConfig()
    config.read(fn)
    config.tiff_base = str(tmpdir)
    config.calib_base = str(tmpdir)
    an_db = config.an_db
    cb = mod.XPDRouter(config)
    for name, doc in raw_db[-1].canonical(fill="yes", strict_order=True):
        cb(name, doc)
    tiff_base = Path(config.tiff_base)
    assert len(list(tiff_base.rglob("*.tiff"))) > 0
    assert len(list(tiff_base.rglob("*.json"))) > 0
    assert len(list(tiff_base.rglob("*.csv"))) > 0
    assert len(list(an_db)) > 0
