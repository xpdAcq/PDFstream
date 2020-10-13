import numpy as np
import pytest

import pdfstream.pipeline.process as mod


@pytest.mark.parametrize(
    "img, bg_img, dk_img",
    [
        ("black_img", None, None),
        ("white_img", "white_img", None),
        ("white_img", None, "white_img"),
    ]
)
def test_reduce(test_data, img, bg_img, dk_img):
    npt = 64
    result = mod.reduce(
        test_data['ai'],
        test_data.get(img, None),
        test_data.get(dk_img, None),
        test_data.get(bg_img, None),
        mask_setting="OFF",
        integ_setting={'npt': npt}
    )
    chi = result[0]
    assert np.array_equal(chi[1], np.zeros(npt))
