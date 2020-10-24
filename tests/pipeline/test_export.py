from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an
import pdfstream.pipeline.export as mod
from pdfstream.pipeline.preprocess import basic_doc_stream

fn = resource_filename("tests", "configs/analysis.ini")
fn1 = resource_filename("tests", "configs/export.ini")


def test_Exporter(run0, tmpdir):
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    config1 = mod.ExportConfig()
    config1.read(fn1)
    config1.set("FILE SYSTEM", "tiff_base", str(tmpdir))
    ep = mod.Exporter(config1)
    ld.subscribe(ep)
    for name, doc in basic_doc_stream(run0):
        ld(name, doc)
    run_dirs = tmpdir.listdir()
    assert len(run_dirs) == 1
    data_dirs = run_dirs[0].listdir()
    assert len(data_dirs) == 3
    assert len(run_dirs[0].join("metadata").listdir()) == 1
    assert len(run_dirs[0].join("images").listdir()) == 2
    assert len(run_dirs[0].join("datasheets").listdir()) == 1
