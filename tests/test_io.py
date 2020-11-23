import numpy as np
import pyFAI
import pytest

from pdfstream.io import load_dict_from_poni, load_ai_from_calib_result


@pytest.fixture(scope="module")
def expect_qi(test_data):
    ai = pyFAI.load(test_data["Ni_poni_file"])
    q, i = ai.integrate1d(test_data['white_img'], 1024, safe=False)
    return q, i


def test_load_dict_from_poni(test_data, expect_qi):
    config = load_dict_from_poni(test_data["Ni_poni_file"])
    ai = pyFAI.AzimuthalIntegrator()
    ai.set_config(config)
    q, i = ai.integrate1d(test_data['white_img'], 1024, safe=False)
    assert np.array_equal(q, expect_qi[0])
    assert np.array_equal(i, expect_qi[1])


def test_load_ai_from_calib_result(test_data):
    dct = test_data['start_doc']
    load_ai_from_calib_result(dct)
