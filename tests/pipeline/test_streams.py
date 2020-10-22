import rapidz as rz

import pdfstream.pipeline.streams as mod
from pdfstream.pipeline.preprocess import basic_doc_stream


def test_doc_preprocess(run0):
    source = rz.Stream()
    nodes = mod.doc_preprocess(source)
    lst = nodes[-1].sink_to_list()
    for doc in basic_doc_stream(run0):
        source.emit(doc)
    doc_types = [item[0] for item in lst]
    assert doc_types == ["start", "descriptor", "event", "stop"]
