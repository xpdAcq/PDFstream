import pdfstream.pipeline.preprocess as mod


def test_basic_doc_stream(run0):
    for name, doc in mod.basic_doc_stream(run0):
        assert name in ["start", "descriptor", "event", "stop"]
        assert isinstance(doc, dict)
        print(name, doc)
