import pytest
from pdfstream.parsers.fitresult import to_xarray, to_latex, rename_rule
from pdfstream.parsers.fitrecipe import recipe_to_dict2


def test_to_latex(recipe):
    dct = recipe_to_dict2(recipe)
    result = to_xarray(dct, ("conresults", 0, "name"))
    df = result.to_dataframe()
    latex = to_latex(("Ni0", df), ("Ni1", df))
    print(latex)


@pytest.mark.parametrize(
    "name, expect",
    [
        ("G0_scale", "scale"),
        ("G0_delta1", r"$\delta_1$ ($\mathrm{\AA}$)"),
        ("G0_delta2", r"$\delta_2$ ($\mathrm{\AA}^2$)"),
        ("G0_a", r"a ($\mathrm{\AA}$)"),
        ("G0_alpha", r"$\alpha$ (deg)"),
        ("G0_Ni0_Biso", r"B$_{iso}$(Ni0) ($\mathrm{\AA}^2$)"),
        ("G0_Ni0_x", r"x(Ni0) ($\mathrm{\AA}$)")
    ]
)
def test_rename_rule(name, expect):
    real = rename_rule(name)
    assert real == expect
