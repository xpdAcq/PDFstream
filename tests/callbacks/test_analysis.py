from configparser import Error
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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
    if use_db:
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
    config.raw_db = db
    ld = an.AnalysisStream(config)
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


def test_ExporterXpdan(db_with_dark_and_scan, tmpdir):
    """Test ExporterXpaan. It should output the correct files in a two layer directory."""
    db = db_with_dark_and_scan
    config = an.AnalysisConfig()
    config.read(fn)
    config.raw_db = db
    ld = an.AnalysisStream(config)
    ep_config = pdfstream.callbacks.analysis.ExportConfig()
    ep_config.read(fn)
    ep_config.tiff_base = str(tmpdir)
    ep = pdfstream.callbacks.analysis.ExporterXpdan(ep_config)
    ld.subscribe(ep)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)
    tiff_base = Path(ep_config.tiff_base)
    data_folder = tiff_base.joinpath("Ni")
    assert data_folder.is_dir()
    for dir_name in ("dark_sub", "integration", "meta", "mask", "iq", "sq", "fq", "pdf", "scalar_data"):
        assert data_folder.joinpath(dir_name).is_dir()
        assert len(list(data_folder.joinpath(dir_name).glob("*.*"))) > 0


def test_ExportConfig():
    config = pdfstream.callbacks.analysis.ExportConfig()
    config.read(fn)
    with pytest.raises(Error):
        assert config.tiff_base


@pytest.fixture(params=[0, 1])
def cases0(request, test_data):
    """Gives user_config dictionary, tuple of property values."""
    if request.param == 0:
        return (
            {"user_config": {"auto_mask": False, "mask_file": test_data["white_img_file"]}},
            (False, test_data["white_img"])
        )
    elif request.param == 1:
        return {}, (True, None)


def test_UserConfig(cases0):
    start_doc, results = cases0
    user_config = an.UserConfig()
    user_config.read_start_doc(start_doc)
    assert user_config.do_auto_masking == results[0]
    assert np.array_equal(user_config.user_mask, results[1])
