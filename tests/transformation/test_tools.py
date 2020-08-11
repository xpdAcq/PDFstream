import numpy
import pytest

from pdfstream.transformation.tools import make_pdfgetter, use_pdfgetter


def test_make_pdfgetter(db):
    make_pdfgetter(
        db['Ni_config'], {'qmin': 1.}
    )


def test_use_pdfgetter(db):
    use_pdfgetter(db['Ni_chi'], db['Ni_pdfgetter'])


@pytest.mark.parametrize(
    "wrong_data",
    [
        numpy.zeros((2, 5, 1)),
        numpy.zeros((5, 2))
    ]
)
def test_use_pdfgetter_error(db, wrong_data):
    with pytest.raises(ValueError):
        use_pdfgetter(wrong_data, db['Ni_pdfgetter'])
