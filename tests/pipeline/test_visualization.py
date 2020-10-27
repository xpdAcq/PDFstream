from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an
import pdfstream.pipeline.visualization as vis

fn = resource_filename("tests", "configs/analysis.ini")
fn1 = resource_filename("tests", "configs/visualization.ini")


def test_Visualizer(db_with_dark_and_light):
    db = db_with_dark_and_light
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config, db=db)
    config1 = vis.VisConfig()
    config1.read(fn1)
    cb = vis.Visualizer(config1)
    ld.subscribe(cb)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)
