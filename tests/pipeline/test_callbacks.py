import pdfstream.pipeline.callbacks as mod


def test_StripDepVar(run0):
    for doc in run0.canonical(fill="yes"):
        cb = mod.StripDepVar()
        doc1 = cb(*doc)
        print(*doc1)
