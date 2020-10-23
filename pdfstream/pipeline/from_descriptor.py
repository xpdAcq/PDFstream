import typing as tp

from .errors import ValueNotFoundError


def find_one_array(data_keys: dict) -> str:
    """Fina one array in the data."""
    for key, value in data_keys.items():
        if value["dtype"] == "array":
            return key
    raise ValueNotFoundError("Array not found in {}".format(data_keys.keys()))


def find_one_image(descriptor: tp.Dict[str, dict]) -> str:
    """Find the key of image data in descriptor."""
    for key, dct in descriptor["data_keys"].items():
        if dct["dtype"] == "array" and _is_image(dct["shape"]):
            return key
    raise ValueNotFoundError("No image array found in descriptor (uid: {})".format(descriptor["uid"]))


def _is_image(shape: list) -> bool:
    """Whether the shape has 2 dimension that has rank larger than 1."""
    return sum([1 for s in shape if s > 1]) == 2
