from pprint import pprint

import mongomock
import pytest
from mongomock.collection import Collection

from pdfstream.parsers.fitrecipe import recipe_to_dict


@pytest.mark.parametrize(
    'data_key', ['pyobjcryst', 'diffpy']
)
def test_recipe_to_dict(recipes, data_key):
    client = mongomock.MongoClient()
    collection: Collection = client.db.collection
    dct = recipe_to_dict(recipes[data_key])
    pprint(dct)
    # test db friendly
    collection.insert_one(dct)
