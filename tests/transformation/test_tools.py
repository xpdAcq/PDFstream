import numpy
import pytest

from pdfstream.transformation.tools import make_pdfgetter, use_pdfgetter


def test_make_pdfgetter(test_data):
    make_pdfgetter(
        test_data['Ni_config'], {'qmin': 1.}
    )


def test_use_pdfgetter(test_data):
    use_pdfgetter(test_data['Ni_chi'], test_data['Ni_pdfgetter'])


@pytest.mark.parametrize(
    "wrong_data",
    [
        numpy.zeros((2, 5, 1)),
        numpy.zeros((5, 2))
    ]
)
def test_use_pdfgetter_error(test_data, wrong_data):
    with pytest.raises(ValueError):
        use_pdfgetter(wrong_data, test_data['Ni_pdfgetter'])
