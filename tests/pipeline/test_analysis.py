from bluesky.callbacks.broker import LiveImage
from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an
from pdfstream.pipeline.preprocess import basic_doc_stream

fn = resource_filename("pdfstream", "data/analysis.ini")


def see_image(live_image: LiveImage):
    fig = live_image.cs._fig
    fig.show()
    return


def test_AnalysisStream(run0):
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    vis = LiveImage(config.data_keys["masked_image"])
    ld.subscribe(vis)
    for name, doc in basic_doc_stream(run0):
        ld(name, doc)
    see_image(vis)
