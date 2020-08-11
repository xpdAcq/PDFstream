"""The tools to read, write, audit, transform, wash the data."""
import pickle
from typing import Any
from typing import Callable
from typing import Generator

from bson.binary import Binary
from numpy import ndarray


def dump_ndarray(arr: ndarray):
    """Pickle dump the numpy array to Binary format."""
    return Binary(pickle.dumps(arr, protocol=2))


def load_binary(binary: Binary):
    """Pickle load the Binary format data."""
    return pickle.loads(binary)


def paths(dct: Any, path=()) -> Generator:
    """Yield paths to the leafs of a nested dictionary."""
    if isinstance(dct, dict):
        for key, value in dct.items():
            yield from paths(value, path + (key,))
    elif isinstance(dct, (tuple, list)):
        for ind, elem in enumerate(dct):
            yield from paths(elem, path + (ind,))
    else:
        yield path + (dct,)


def iter_dct(dct: dict, operation: Callable):
    """Recursively iterate the dictionary and operate on the leaf nodes. Return the processed dictionary."""
    dct2 = dict()
    for key, value in dct.items():
        if isinstance(value, dict):
            dct2[key] = iter_dct(value, operation)
        else:
            dct2[key] = operation(value)
    return dct2


def from_db(dct: dict):
    """Wash the data in the dictionary loaded from mongodb so that they can be in correct format."""

    def wash(item):
        return load_binary(item) if isinstance(item, Binary) else item

    return iter_dct(dct, wash)


def to_db(dct: dict):
    """Wash the data that will go to mongodb so that they can be in correct format."""

    def wash(item):
        return dump_ndarray(item) if isinstance(item, ndarray) else item

    return iter_dct(dct, wash)


def to_dict(obj: object, exclude: Callable[[str], bool] = None) -> dict:
    """Convert an object to a dictionary by keeping import attribute information."""

    def pdfconfig_exclude(attr: str) -> bool:
        """Whether to exclude an attribute in pdfconfig."""
        if attr.startswith("_"):
            return True
        if attr in ("inputfiles", "output", "interact"):
            return True
        return False

    dct = {}
    if exclude is None:
        exclude = pdfconfig_exclude
    for attr_key, attr_val in obj.__dict__.items():
        if not exclude(attr_key):
            dct[attr_key] = attr_val
    return dct
