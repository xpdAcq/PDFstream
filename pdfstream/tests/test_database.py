import pytest

from pdfstream.database.tools import recipe_to_dict
from pdfstream.modeling.main import multi_phase, MyParser, optimize


@pytest.fixture(scope="module")
def recipe(db):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    phases = [db['Ni_stru']]
    recipe = multi_phase(phases, parser, fit_range=(0., 8., .1))
    optimize(recipe, ['all'])
    return recipe


def test_recipe_to_dict(recipe):
    dct = recipe_to_dict(recipe)
    assert isinstance(dct, dict)
