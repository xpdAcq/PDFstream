import pdfstream.callbacks.basic as mod


def test_NumpyExporter(tmpdir, array_stream):
    cb = mod.NumpyExporter(str(tmpdir), file_prefix="{start[sample_name]}_")
    for name, doc in array_stream:
        cb(name, doc)
    assert len(tmpdir.listdir()) > 0


def test_StackedNumpyExporter(tmpdir, array_stream):
    cb = mod.StackedNumpyExporter(str(tmpdir), file_prefix="{start[sample_name]}_", data_keys=["x0"])
    for name, doc in array_stream:
        cb(name, doc)
    assert len(tmpdir.listdir()) > 0


def test_StackedNumpyTextExporter(tmpdir, array_stream):
    cb = mod.StackedNumpyTextExporter("{start[sample_name]}_", str(tmpdir), ["x0"], ".x0")
    for name, doc in array_stream:
        cb(name, doc)
    assert len(tmpdir.listdir()) > 0


def test_DataFrameExporter(tmpdir, array_stream):
    cb = mod.DataFrameExporter(str(tmpdir), file_prefix="{start[sample_name]}_")
    for name, doc in array_stream:
        cb(name, doc)
    assert len(tmpdir.listdir()) > 0


def test_SmartScalarPlot(ymax_stream):
    cb = mod.SmartScalarPlot("ymax")
    for name, doc in ymax_stream:
        cb(name, doc)
    cb.show()
