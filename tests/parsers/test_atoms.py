from pprint import pprint

import pytest

from pdfstream.parsers.atoms import dict_to_atoms
from pdfstream.parsers.fitrecipe import recipe_to_dict


@pytest.mark.parametrize(
    'data_key', ['pyobjcryst', 'diffpy']
)
def test_dict_to_atoms(recipes, data_key):
    dct = recipe_to_dict(recipes[data_key])
    atoms = dict_to_atoms(dct, ("genresults", 0))
    pprint(atoms)
