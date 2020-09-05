import pytest

from pdfstream.modeling.adding import initialize


@pytest.mark.parametrize(
    "scale,delta,lat,adp,xyz,params,expect",
    [
        (
                True, None, None, None, None, None,
                {"scale_G0"}
        ),
        (
                False, "1", None, None, None, None,
                {"delta1_G0"}
        ),
        (
                False, "2", None, None, None, None,
                {"delta2_G0"}
        ),
        (
                False, None, "s", None, None, None,
                {"a_G0"}
        ),
        (
                False, None, "a", None, None, None,
                {"a_G0", "b_G0", "c_G0", "alpha_G0", "beta_G0", "gamma_G0"}
        ),
        (
                False, None, None, "e", None, None,
                {"Biso_Ni_G0"}
        ),
        (
                False, None, None, "a", None, None,
                {"Biso_Ni0_G0"}
        ),
        (
                False, None, None, "s", None, None,
                {"Biso_Ni0_G0"}
        ),
        (
                False, None, None, None, "s", None,
                set()
        ),
        (
                False, None, None, None, "a", None,
                {"x_Ni0_G0", "y_Ni0_G0", "z_Ni0_G0"}
        ),
        (
                False, None, None, None, None, "a",
                {"A", "psize_f0"}
        ),
        (
                False, None, None, None, None, ["A"],
                {"A"}
        ),
        pytest.param(
            False, "haha", None, None, None, None, set(),
            marks=pytest.mark.xfail
        ),
        pytest.param(
            False, None, "haha", None, None, None, set(),
            marks=pytest.mark.xfail
        ),
        pytest.param(
            False, None, None, "haha", None, None, set(),
            marks=pytest.mark.xfail
        ),
        pytest.param(
            False, None, None, None, "haha", None, set(),
            marks=pytest.mark.xfail
        ),
        pytest.param(
            False, None, None, None, None, "haha", set(),
            marks=pytest.mark.xfail
        ),
    ]
)
def test_initialize(blank_recipe, scale, delta, lat, adp, xyz, params, expect):
    initialize(blank_recipe, scale, delta, lat, adp, xyz, params)
    assert set(blank_recipe.getNames()) == expect
