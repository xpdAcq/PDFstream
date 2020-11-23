from configparser import Error
from pathlib import Path

import matplotlib.pyplot as plt
import pytest
from pkg_resources import resource_filename

import pdfstream.callbacks
import pdfstream.callbacks.analysis as an
from pdfstream.schemas import analysis_out_schemas, analysis_in_schemas, Validator

fn = resource_filename("tests", "configs/xpd_server.ini")


@pytest.mark.parametrize("use_db", [True, False])
def test_AnalysisStream(db_with_img_and_bg_img, use_db):
    db = db_with_img_and_bg_img
    config = an.AnalysisConfig()
    config.read(fn)
    config.raw_db = db
    ld = an.AnalysisStream(config)
    # validate that output data
    out_validator = Validator(analysis_out_schemas)
    ld.subscribe(out_validator)
    # validate the input data
    in_validator = Validator(analysis_in_schemas)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        in_validator(name, doc)
        ld(name, doc)


def test_Visualizer(db_with_dark_and_scan):
    db = db_with_dark_and_scan
    config = an.AnalysisConfig()
    config.raw_db = db
    config.read(fn)
    ld = an.AnalysisStream(config)
    config1 = pdfstream.callbacks.analysis.VisConfig()
    config1.read(fn)
    config1.fig = plt.figure()
    cb = pdfstream.callbacks.analysis.Visualizer(config1)
    ld.subscribe(cb)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)
    cb.show_figs()


def test_Exporter(db_with_dark_and_scan, tmpdir):
    db = db_with_dark_and_scan
    config = an.AnalysisConfig()
    config.read(fn)
    config.raw_db = db
    ld = an.AnalysisStream(config)
    ep_config = pdfstream.callbacks.analysis.ExportConfig()
    ep_config.read(fn)
    ep_config.tiff_base = str(tmpdir)
    ep = pdfstream.callbacks.analysis.Exporter(ep_config)
    ld.subscribe(ep)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
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
