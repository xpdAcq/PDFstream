import matplotlib.pyplot as plt
import numpy as np
import pytest

import pdfstream.integration.masking as masking


@pytest.fixture
def user_mask(request, db):
    if request.param == "ones":
        return np.ones_like(db["Ni_img"])
    if request.param == "zeros":
        return np.zeros_like(db["Ni_img"])
    return None


@pytest.mark.parametrize(
    "user_mask, mask_setting",
    [
        (None, None),
        (None, {"alpha": 2, "upper_thresh": 1000}),
        ("ones", None),
        ("zeros", None)
    ],
    indirect=["user_mask"]
)
def test_auto_mask(db, user_mask, mask_setting):
    mask, _ = masking.auto_mask(db['Ni_img'], db['ai'], user_mask=user_mask, mask_setting=mask_setting)
    plt.matshow(mask)
    plt.colorbar()
    plt.show(block=False)
    plt.close()
