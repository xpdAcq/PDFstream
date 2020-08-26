from pprint import pprint

import pytest
from mongomock import MongoClient

import pdfstream.parsers as ctd


@pytest.mark.parametrize(
    "kwargs",
    [
        {"mmjson": True},
        {"mmjson": False}
    ]
)
def test_cif_to_dict(db, kwargs):
    client = MongoClient()
    coll = client.db.coll
    dcts = ctd.cif_to_dict(
        db["Ni_stru_file"],
        **kwargs
    )
    for dct in dcts:
        pprint(dct)
        # test mongo friendly
        coll.insert_one(dct)
