from .errors import ValueNotFoundError


def find_one_array(data_keys: dict) -> str:
    """Fina one array in the data."""
    for key, value in data_keys.items():
        if value["dtype"] == "array":
            return key
    raise ValueNotFoundError("Array not found in {}".format(data_keys.keys()))
