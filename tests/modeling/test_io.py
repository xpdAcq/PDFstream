import pytest

from pdfstream.modeling.io import loadData


@pytest.mark.parametrize(
    "meta",
    [
        {},
        {"qdamp": 0.04, "qbroad": 0.02},
        {"qmin": 0.}
    ]
)
def test_load_data(db, meta):
    parser = loadData(db["Ni_gr_file"], meta)
    assert parser
