from pprint import pprint

import mongomock
import pytest
from mongomock.collection import Collection

from pdfstream.parsers.fitrecipe import recipe_to_dict, recipe_to_dict2
from pdfstream.parsers.atoms import dict_to_atoms, dict_to_atoms2
from ase.visualize import view


def test_recipe_to_dict(recipe):
    client = mongomock.MongoClient()
    collection: Collection = client.db.collection
    dct = recipe_to_dict(recipe)
    # test db friendly
    collection.insert_one(dct)
    dict_to_atoms(collection.find_one())


def test_recipe_to_dict2(recipe):
    client = mongomock.MongoClient()
    collection: Collection = client.db.collection
    dct = recipe_to_dict2(recipe)
    collection.insert_one(dct)
    dict_to_atoms2(collection.find_one())
