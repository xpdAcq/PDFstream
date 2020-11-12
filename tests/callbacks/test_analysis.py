import pytest
from configparser import Error
from pathlib import Path
from pkg_resources import resource_filename

import pdfstream.callbacks
import pdfstream.callbacks.analysis as an
from pdfstream.callbacks import analysis as an

fn = resource_filename("tests", "configs/xpd_server.ini")


@pytest.mark.parametrize("use_db", [True, False])
def test_AnalysisStream(db_with_dark_and_light, use_db):
    db = db_with_dark_and_light
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config, raw_db=db if use_db else None)
    ld.subscribe(print)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)


def test_Visualizer(db_with_dark_and_light):
    db = db_with_dark_and_light
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config, raw_db=db)
    config1 = pdfstream.callbacks.analysis.VisConfig()
    config1.read(fn)
    cb = pdfstream.callbacks.analysis.Visualizer(config1)
    ld.subscribe(cb)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)


def test_Exporter(db_with_dark_and_scan, tmpdir):
    raw_db = db_with_dark_and_scan
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    ep_config = pdfstream.callbacks.analysis.ExportConfig()
    ep_config.read(fn)
    ep_config.tiff_base = str(tmpdir)
    ep = pdfstream.callbacks.analysis.Exporter(ep_config)
    ld.subscribe(ep)
    for name, doc in raw_db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)
    tiff_base = Path(ep_config.tiff_base)
    assert len(list(tiff_base.rglob("*.tiff"))) > 0
    assert len(list(tiff_base.rglob("*.csv"))) > 0
    assert len(list(tiff_base.rglob("*.json"))) > 0


def test_ExportConfig():
    config = pdfstream.callbacks.analysis.ExportConfig()
    config.read(fn)
    with pytest.raises(Error):
        assert config.tiff_base
