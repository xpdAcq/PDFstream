import pytest
from pdfstream.parsers.dict_to_atoms import dict_to_atoms
from pdfstream.parsers.recipe_to_dict import recipe_to_dict
from pprint import pprint


@pytest.mark.parametrize(
    'data_key', ['pyobjcryst', 'diffpy']
)
def test_dict_to_atoms(recipes, data_key):
    dct = recipe_to_dict(recipes[data_key])
    atoms = dict_to_atoms(dct, ("genresults", 0))
    pprint(atoms)
