import numpy as np

from pdfstream.utils.parse import load_poni, paths, from_db, to_db, to_dict


def test_load_poni(db):
    poni_file = db.get('Ni_poni_file')
    black_img = db.get('black_img')
    config = load_poni(poni_file)
    from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
    ai0 = AzimuthalIntegrator()
    ai0.set_config(config)
    q0, i0 = ai0.integrate1d(black_img, 1024, safe=False)
    import pyFAI
    ai1 = pyFAI.load(poni_file)
    q1, i1 = ai1.integrate1d(black_img, 1024, safe=False)
    assert np.array_equal(q0, q1)
    assert np.array_equal(i0, i1)


def test_paths():
    dct = {
        "k1": {
            "k11": "v11",
            "k12": {
                "k121": "v121"
            }
        },
        "k2": ["v21", "v22"]
    }
    assert list(paths(dct)) == [
        ("k1", "k11", "v11"),
        ("k1", "k12", "k121", "v121"),
        ("k2", 0, "v21"),
        ("k2", 1, "v22")
    ]


def test_from_db_and_to_db():
    from bson.binary import Binary
    original = {
        'img': {
            'data': np.zeros((2, 2)),
            'meta': {'a': 1, 'b': 2}
        }
    }
    doc = to_db(original)
    dct = from_db(doc)
    assert isinstance(doc['img']['data'], Binary)
    assert np.array_equal(dct['img']['data'], original['img']['data'])


def test_to_dict(db):
    to_dict(db["Ni_config"])
