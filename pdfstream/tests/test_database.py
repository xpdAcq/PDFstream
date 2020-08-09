import mongomock
import pytest
from diffpy.structure import loadStructure
from mongomock.collection import Collection
from pyobjcryst import loadCrystal

from pdfstream.database.recipe_to_dict import recipe_to_dict
from pdfstream.modeling.main import multi_phase, MyParser, optimize


@pytest.fixture(scope="module")
def recipes(db):
    """A recipe of crystal in pyobjcryst."""
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    # a recipe of crystal in pyobjcryst
    phases0 = [loadCrystal(db['Ni_stru_file'])]
    recipe0 = multi_phase(phases0, parser, fit_range=(3., 8., .2))
    optimize(recipe0, ['all'])
    # a recipe of structure in diffpy.structure
    phases1 = [loadStructure(db['Ni_stru_file'])]
    recipe1 = multi_phase(phases1, parser, fit_range=(3., 8., .2), sg_params={'G0': 225})
    optimize(recipe1, ['all'])
    return {
        'pyobjcryst': recipe0,
        'diffpy': recipe1
    }


@pytest.mark.parametrize(
    'data_key', ['pyobjcryst', 'diffpy']
)
def test_recipe_to_dict(recipes, data_key):
    client = mongomock.MongoClient()
    collection: Collection = client.db.collection
    dct = recipe_to_dict(recipes[data_key])
    # test db friendly
    collection.insert_one(dct)
