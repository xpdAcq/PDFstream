from configparser import Error
from pathlib import Path

import pytest
from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an
import pdfstream.pipeline.export as mod

fn = resource_filename("tests", "configs/analysis.ini")
fn1 = resource_filename("tests", "configs/export.ini")


def test_ExportConfig():
    config = mod.ExportConfig()
    config.read(fn1)
    with pytest.raises(Error):
        assert config.tiff_base


def test_Exporter(db_with_dark_and_scan, tmpdir):
    raw_db = db_with_dark_and_scan
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    ep_config = mod.ExportConfig()
    ep_config.read(fn1)
    ep_config.tiff_base = str(tmpdir)
    ep = mod.Exporter(ep_config)
    ld.subscribe(ep)
    for name, doc in raw_db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)
    tiff_base = Path(ep_config.tiff_base)
    assert len(list(tiff_base.rglob("*.tiff"))) > 0
    assert len(list(tiff_base.rglob("*.csv"))) > 0
    assert len(list(tiff_base.rglob("*.json"))) > 0
