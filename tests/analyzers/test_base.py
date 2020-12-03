import databroker
import pytest

import pdfstream.analyzers.base as mod
from pdfstream.callbacks.composer import gen_stream


@pytest.fixture(scope="function")
def db_with_fake_an():
    """A database that has a fake analysis run."""
    db = databroker.v2.temp()
    for name, doc in gen_stream([], {"an_config": {"SECTION": {"key": "value"}}}):
        db.v1.insert(name, doc)
    return db


def test_AnalyzerConfig(db_with_fake_an):
    db = db_with_fake_an
    config = mod.AnalyzerConfig()
    config.read_run(db[-1])
    assert config.sections() == ["SECTION"]
    assert config["SECTION"]["key"] == "value"


def test_Analyzer(db_with_fake_an):
    db = db_with_fake_an
    analyzer = mod.Analyzer()
    analyzer.analyze(db[-1])
