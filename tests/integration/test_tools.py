import matplotlib.pyplot as plt
import numpy as np
import pytest

import pdfstream.integration.tools
import pdfstream.integration.tools as tools
from pdfstream.integration.tools import integrate


def test_bg_sub_error():
    with pytest.raises(ValueError):
        tools.bg_sub(np.ones((2, 2)), np.zeros((3, 3)))


@pytest.mark.parametrize(
    "case", [0]
)
def test_integrate(db, case):
    if case == 0:
        chi, setting = integrate(
            db["Ni_img"], db["ai"], mask=np.ones_like(db["Ni_img"]), integ_setting={"npt": 1000}
        )
        expect = np.zeros(1000)
        assert chi.shape == (2, 1000)
        assert np.array_equal(chi[1], expect)


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
    mask, _ = pdfstream.integration.tools.auto_mask(db['Ni_img'], db['ai'], user_mask=user_mask,
                                                    mask_setting=mask_setting)
    plt.matshow(mask)
    plt.colorbar()
    plt.show(block=False)
    plt.close()
