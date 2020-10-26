import pdfstream.pipeline.callbacks as mod


def test_StartStopCallback(simple_stream):
    cb = mod.StartStopCallback()
    for name, doc in simple_stream:
        cb(name, doc)
