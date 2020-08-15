import typing as tp


def get_value(dct: dict, keys: tuple) -> tp.Any:
    """Get the value by walking along a key chain."""
    result = dct
    for key in keys:
        result = result[key]
    return result
