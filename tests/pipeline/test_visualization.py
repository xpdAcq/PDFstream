from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an
import pdfstream.pipeline.visualization as vis
from pdfstream.pipeline.preprocess import basic_doc_stream

fn = resource_filename("tests", "configs/analysis.ini")
fn1 = resource_filename("tests", "configs/visualization.ini")


def test_Visualizer(run0):
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    config1 = vis.VisConfig()
    config1.read(fn1)
    cb = vis.Visualizer(config1)
    ld.subscribe(cb)
    for name, doc in basic_doc_stream(run0):
        ld(name, doc)
