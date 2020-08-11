import pytest

from pdfstream.modeling.fitfuncs import make_generator, get_sgpars
from pdfstream.modeling.fitobjs import GenConfig


@pytest.mark.parametrize(
    "kwargs",
    [
        {"ncpu": 1}
    ]
)
def test_make_generator(db, kwargs):
    gen_config = GenConfig("G0", db['Ni_stru'], **kwargs)
    make_generator(gen_config)


@pytest.mark.parametrize(
    "arg", ["P1"]
)
def test_get_sgpars(recipe, arg):
    con = next(iter(recipe.contributions.values()))
    gen = next(iter(con.generators.values()))
    get_sgpars(gen.phase, arg)


def test_get_sgpars_error(recipe, db):
    with pytest.raises(ValueError):
        get_sgpars(db['Ni_stru'])
