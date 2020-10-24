from bluesky.callbacks.broker import LiveImage
from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an
import pdfstream.pipeline.visualization as vis
from pdfstream.pipeline.preprocess import basic_doc_stream
from pdfstream.pipeline.visualization import LiveWaterfall

fn = resource_filename("tests", "configs/analysis.ini")


def see_image(live_image: LiveImage):
    fig = live_image.cs._fig
    fig.show()


def see_figure(live_waterfall: LiveWaterfall):
    fig = live_waterfall.waterfall.fig
    if fig:
        fig.show()


def test_gen_vis_cbs(run0):
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    cbs = list(vis.gen_vis_cbs())
    for cb in cbs:
        ld.subscribe(cb)
    for name, doc in basic_doc_stream(run0):
        ld(name, doc)
        if name == "event":
            see_image(cbs[1])
            see_figure(cbs[2])
            see_figure(cbs[3])
            see_figure(cbs[4])
