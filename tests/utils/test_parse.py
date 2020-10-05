from pdfstream.utils.parse import paths, to_dict


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


def test_to_dict(db):
    to_dict(db["Ni_config"])
