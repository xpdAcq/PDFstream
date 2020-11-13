import pdfstream.callbacks.basic as mod


def test_StartStopCallback(simple_stream):
    cb = mod.StartStopCallback()
    for name, doc in simple_stream:
        cb(name, doc)


def test_SmartScalarPlot(ymax_stream):
    cb = mod.SmartScalarPlot("ymax")
    for name, doc in ymax_stream:
        cb(name, doc)
    cb.show()
