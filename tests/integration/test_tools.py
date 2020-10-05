import numpy as np
import pytest

import pdfstream.integration.tools as tools
from pdfstream.integration.masking import auto_mask
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


def test_auto_mask(db):
    mask, _ = auto_mask(db["Ni_img"], db["ai"])
    assert np.array_equal(mask[0], np.ones_like(mask[0]))
