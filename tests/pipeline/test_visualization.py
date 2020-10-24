from bluesky.callbacks.broker import LiveImage
from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an
import pdfstream.pipeline.visualization as vis
from pdfstream.pipeline.preprocess import basic_doc_stream
from pdfstream.pipeline.visualization import LiveWaterfall

fn = resource_filename("tests", "configs/analysis.ini")
fn1 = resource_filename("tests", "configs/vis.ini")


def see_image(live_image: LiveImage):
    fig = live_image.cs._fig
    fig.show()


def see_figure(live_waterfall: LiveWaterfall):
    fig = live_waterfall.waterfall.fig
    if fig:
        fig.show()


def test_VisRunRouter(run0):
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config)
    config1 = vis.VisConfig()
    config1.read(fn1)
    lv = vis.VisRunRouter(config1)
    ld.subscribe(lv)
    for name, doc in basic_doc_stream(run0):
        ld(name, doc)
        if name == "event":
            see_image(lv.cb_lst[0])
            see_figure(lv.cb_lst[1])
            see_figure(lv.cb_lst[2])
            see_figure(lv.cb_lst[3])
