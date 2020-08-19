import pdfstream.parsers as ctd
from mongomock import MongoClient
from pprint import pprint


def test_cif_to_dict(db):
    client = MongoClient()
    coll = client.db.coll
    dcts = ctd.cif_to_dict(
        db["Ni_stru_file"]
    )
    for dct in dcts:
        pprint(dct)
        # test mongo friendly
        coll.insert_one(dct)
