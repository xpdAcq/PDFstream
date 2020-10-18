from .errors import ValueNotFoundError


def find_one_array(data_keys: dict, ndim: int = 2) -> str:
    for key, value in data_keys.items():
        if value["dtype"] == "array" or (
            value["dtype"] in ("number", "integar") and len(value["shape"]) == ndim
        ):
            return key
    raise ValueNotFoundError("2D array not found in {}".format(data_keys.keys()))
