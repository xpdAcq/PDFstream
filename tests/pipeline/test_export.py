import databroker
import pytest
from configparser import Error
from pathlib import Path
from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an
import pdfstream.pipeline.export as mod
from pdfstream.pipeline.preprocess import basic_doc_stream

fn = resource_filename("tests", "configs/analysis.ini")
fn1 = resource_filename("tests", "configs/export.ini")


@pytest.fixture(params=["temp", pytest.param("none", marks=pytest.mark.xfail(raises=Error))])
def ep_config(request, tmpdir):
    config = mod.ExportConfig()
    config.read(fn1)
    if request.param == "temp":
        config.tiff_base = str(tmpdir)
    if request.param == "none":
        pass
    return config


def test_Exporter(run0, ep_config):
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    db = databroker.v2.temp()
    ep = mod.Exporter(ep_config, test_db=db)
    ld.subscribe(ep)
    for name, doc in basic_doc_stream(run0):
        ld(name, doc)
    tiff_base = Path(ep_config.tiff_base)
    assert len(list(tiff_base.iterdir())) == 1
    run_dir = next(tiff_base.iterdir())
    assert len(list(run_dir.joinpath("metadata").iterdir())) == 1
    assert len(list(run_dir.joinpath("images").iterdir())) == 2
    assert len(list(run_dir.joinpath("datasheets").iterdir())) == 1
    assert db[-1]
