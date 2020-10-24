from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an
from pdfstream.pipeline.preprocess import basic_doc_stream

fn = resource_filename("tests", "configs/analysis.ini")


def test_AnalysisStream(run0):
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    for name, doc in basic_doc_stream(run0):
        ld(name, doc)
