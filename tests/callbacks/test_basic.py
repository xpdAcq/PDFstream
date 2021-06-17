import numpy as np

import pdfstream.callbacks.basic as mod
from pdfstream.callbacks.composer import gen_stream


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
    cb = mod.StackedNumpyTextExporter("{start[sample_name]}_", str(tmpdir), ["x0", "x1"], ".x")
    for name, doc in array_stream:
        cb(name, doc)
    files = tmpdir.listdir()
    assert len(files) > 0
    arr = np.loadtxt((files[0]))
    print(arr)


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


def test_CalibrationExporter(tmpdir):
    # case 1
    start = {}
    ce = mod.CalibrationExporter(tmpdir)
    for name, doc in gen_stream([{}], start):
        ce(name, doc)
    files = tmpdir.listdir()
    assert len(files) == 0
    # case 2
    start = {"calibration_md": {"distance": 2, "wavelength": 2}}
    for name, doc in gen_stream([{}], start):
        ce(name, doc)
    files = tmpdir.listdir()
    assert len(files) > 0
    print(files[0].read_text(encoding="utf-8"))
