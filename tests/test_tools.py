import numpy as np
import pytest

from pdfstream.integration.tools import integrate


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
