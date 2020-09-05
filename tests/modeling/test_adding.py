import pytest

from pdfstream.modeling.adding import initialize


@pytest.mark.parametrize("scale", [True, False])
@pytest.mark.parametrize("delta", ["1", "2", None])
@pytest.mark.parametrize("lat", ["s", "a"])
@pytest.mark.parametrize("adp", ["a", "e", "s"])
@pytest.mark.parametrize("xyz", ["s", "a"])
@pytest.mark.parametrize("params", [None, "ALL", ["A"]])
def test_initialize(blank_recipe, scale, delta, lat, adp, xyz, params):
    initialize(blank_recipe, scale, delta, lat, adp, xyz, params)
