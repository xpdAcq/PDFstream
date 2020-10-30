import pytest
from pkg_resources import resource_filename

import pdfstream.pipeline.analysis as an

fn = resource_filename("tests", "configs/analysis.ini")


@pytest.mark.parametrize("use_db", [True, False])
def test_AnalysisStream(db_with_dark_and_light, use_db):
    db = db_with_dark_and_light
    config = an.AnalysisConfig()
    config.read(fn)
    ld = an.AnalysisStream(config, raw_db=db if use_db else None)
    ld.subscribe(print)
    for name, doc in db[-1].canonical(fill="yes", strict_order=True):
        ld(name, doc)
