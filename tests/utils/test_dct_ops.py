import pytest

import pdfstream.utils.dct_ops as dct_ops


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
    assert list(dct_ops.paths(dct)) == [
        ("k1", "k11", "v11"),
        ("k1", "k12", "k121", "v121"),
        ("k2", 0, "v21"),
        ("k2", 1, "v22")
    ]


def test_to_dict(test_data):
    dct_ops.to_dict(test_data["Ni_config"])


@pytest.mark.parametrize(
    "dct, op, expect",
    [
        (
            {"k0": {"k1": 0, "k2": 1}},
            lambda x: x + 1,
            {"k0": {"k1": 1, "k2": 2}}
        )
    ]
)
def test_iter_dct(dct, op, expect):
    dct1 = dct_ops.iter_dct(dct, op)
    assert dct1 == expect


@pytest.mark.parametrize(
    "dct, keys, expect",
    [
        ({"k": {"k1": "v"}}, ("k", "k1"), "v"),
        ({"k": "v"}, tuple(), {"k": "v"}),
    ]
)
def test_get_value(dct, keys, expect):
    value = dct_ops.get_value(dct, keys=keys)
    assert value == expect
