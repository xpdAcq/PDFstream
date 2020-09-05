import pytest

from pdfstream.modeling.setting import set_range


@pytest.mark.parametrize(
    "rmin,rmax,rstep",
    [
        (0., 5., 0.1),
        ("obs", "obs", "obs"),
        (None, None, None)
    ]
)
def test_set_range(blank_recipe, rmin, rmax, rstep):
    set_range(blank_recipe)
