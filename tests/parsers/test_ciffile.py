import pdfstream.parsers as ctd
from mongomock import MongoClient


def test_cif_to_dict(db):
    dct = ctd.cif_to_dict(
        db["Ni_stru_file"]
    )
    # test mongo friendly
    client = MongoClient()
    coll = client.db.coll
    coll.insert_one(dct)
