import pytest
from diffpy.srfit.fitbase import FitResults

from pdfstream.database.tools import fitresult_to_dict, structure_to_dict
from pdfstream.modeling.main import multi_phase, MyParser, optimize


@pytest.fixture(scope="module")
def recipe(db):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    phases = [db['Ni_stru']]
    recipe = multi_phase(phases, parser, fit_range=(0., 8., .1))
    optimize(recipe, ['all'])
    return recipe


def test_fitresult_to_dict(recipe):
    result = FitResults(recipe)
    fitresult_to_dict(result)


def test_structure_to_dict(recipe):
    gen = recipe.multi_phase.G0
    structure_to_dict(gen.phase)
