import numpy as np
import pyFAI
import pytest

import pdfstream.io as mod


@pytest.fixture(scope="module")
def expect_qi(test_data):
    ai = pyFAI.load(test_data["Ni_poni_file"])
    q, i = ai.integrate1d(test_data['white_img'], 1024, safe=False)
    return q, i


def test_load_dict_from_poni(test_data, expect_qi):
    config = mod.load_dict_from_poni(test_data["Ni_poni_file"])
    ai = pyFAI.AzimuthalIntegrator()
    ai.set_config(config)
    q, i = ai.integrate1d(test_data['white_img'], 1024, safe=False)
    assert np.array_equal(q, expect_qi[0])
    assert np.array_equal(i, expect_qi[1])


def test_load_ai_from_calib_result(test_data):
    dct = test_data['start_doc']
    mod.load_ai_from_calib_result(dct)


def test_load_matrix_flexible(tmpdir):
    tiff_file = str(tmpdir.join("test.tiff"))
    tif_file = str(tmpdir.join("test.tif"))
    npy_file = str(tmpdir.join("test.npy"))
    txt_file = str(tmpdir.join("test.txt"))
    matrix = np.zeros([3, 3])
    mod.write_tiff(tiff_file, matrix)
    mod.write_tiff(tif_file, matrix)
    np.save(npy_file, matrix)
    np.savetxt(txt_file, matrix)
    for f in [tiff_file, tif_file, npy_file, txt_file]:
        matrix1 = mod.load_matrix_flexible(f)
        assert np.array_equal(matrix1, matrix)


def test_load_matrix_flexible_error():
    with pytest.raises(ValueError):
        mod.load_matrix_flexible("test.jpg")


def test_server_message():
    mod.server_message("test 1")
    mod.quiet()
    mod.server_message("test 2")
    mod.verbose()
    mod.server_message("test 3")
