import numpy as np
import pytest

from pdfstream.parsers.fitdata import dict_to_array


@pytest.mark.parametrize(
    "dct,keys,expected",
    [
        (
                {
                    "result": {
                        "x": [0, 1, 2],
                        "ycalc": [1, 1, 1],
                        "y": [1, 2, 1]
                    }
                },
                ("result",),
                np.array(
                    [[0, 1, 2],
                     [1, 1, 1],
                     [1, 2, 1]]
                )
        )
    ]
)
def test_dict_to_array(dct, keys, expected):
    assert np.array_equal(
        dict_to_array(dct, keys),
        expected
    )
