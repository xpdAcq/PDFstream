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
def test_AnalysisStream(db_with_img_and_bg_img, use_db, tmp_path):
    db = db_with_img_and_bg_img
    config = an.AnalysisConfig()
    config.read(fn)
    config["ANALYSIS"]["tiff_base"] = str(tmp_path)
    ld = an.AnalysisStream(config)
    if use_db:
        ld.db = db.v1
    # validate that output data
    out_validator = Validator(analysis_out_schemas)
    ld.subscribe(out_validator)
    # validate the input data
    in_validator = Validator(analysis_in_schemas)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        in_validator(name, doc)
        # test no numpy array
        ld(name, doc)


@pytest.fixture(params=[0, 1, 2, 3])
def user_config(request, test_data):
    # user gives a mask as the starting point of auto maksing
    if request.param == 0:
        return {"user_mask": test_data["mask_file"]}
    # user just wants to use the mask
    elif request.param == 1:
        return {"auto_mask": False, "user_mask": test_data["mask_file"]}
    # user doesn't care
    elif request.param == 2:
        return {}
    # user doesn't want any masking
    elif request.param == 3:
        return {"auto_mask": False}


def test_AnalysisStream_with_UserConfig(db_with_img_and_bg_img, user_config):
    """Test the analysis stream with user configuration of masking."""
    db = db_with_img_and_bg_img
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    ld.db = db.v1
    # validate that output data
    out_validator = Validator(analysis_out_schemas)
    ld.subscribe(out_validator)
    # validate the input data
    in_validator = Validator(analysis_in_schemas)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        if name == "start":
            doc = dict(**doc, user_config=user_config)
        in_validator(name, doc)
        ld(name, doc)


def test_Visualizer(db_with_dark_and_scan):
    db = db_with_dark_and_scan
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    ld.db = db.v1
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
    ld = an.AnalysisStream(config)
    ld.db = db.v1
    ep_config = pdfstream.callbacks.analysis.ExportConfig()
    ep_config.read(fn)
    ep_config.tiff_base = str(tmpdir)
    ep = pdfstream.callbacks.analysis.Exporter(ep_config)
    ld.subscribe(ep)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)
    tiff_base = Path(ep_config.tiff_base)
    # test the files are output
    assert len(list(tiff_base.rglob("dark_sub/*.tiff"))) > 0
    assert len(list(tiff_base.rglob("mask/*.npy"))) > 0
    assert len(list(tiff_base.rglob("scalar_data/*.csv"))) > 0
    assert len(list(tiff_base.rglob("integration/*.chi"))) > 1
    assert len(list(tiff_base.rglob("meta/*.yml"))) > 0
    assert len(list(tiff_base.rglob("sq/*.sq"))) > 0
    assert len(list(tiff_base.rglob("fq/*.fq"))) > 0
    assert len(list(tiff_base.rglob("gr/*.gr"))) > 0


def test_filenames(db_with_dark_and_scan, tmpdir):
    """Test exported file names and sizes from Exporter."""
    db = db_with_dark_and_scan
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    ld.db = db.v1
    ep_config = pdfstream.callbacks.analysis.ExportConfig()
    ep_config.read(fn)
    ep_config.tiff_base = str(tmpdir)
    ep = pdfstream.callbacks.analysis.Exporter(ep_config)
    ld.subscribe(ep)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)


def test_ExportConfig():
    config = pdfstream.callbacks.analysis.ExportConfig()
    config.read(fn)
    with pytest.raises(Error):
        assert config.tiff_base


def test_user_mask1(db_with_img_and_bg_img):
    db = db_with_img_and_bg_img
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    ld.db = db.v1
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        if name == "start":
            doc = dict(**doc, user_config={"auto_mask": False})
        ld(name, doc)


def test_user_mask2(db_with_img_and_bg_img, test_data):
    db = db_with_img_and_bg_img
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    ld.db = db.v1
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        if name == "start":
            doc = dict(**doc, user_config={"auto_mask": False, "mask_file": test_data["mask_file"]})
        ld(name, doc)
