import typing
import typing as tp

from pdfstream.errors import ValueNotFoundError
from pdfstream.vend.formatters import SpecialStr


def find_one_array(data_keys: dict) -> str:
    """Fina one array in the data."""
    for key, value in data_keys.items():
        if value["dtype"] == "array":
            return key
    raise ValueNotFoundError("Array not found in {}".format(data_keys.keys()))


def yield_1d_array(data_keys: dict) -> tp.Generator[str, None, None]:
    """Fina one array in the data."""
    for key, value in data_keys.items():
        if value["dtype"] == "array" and len(value["shape"]) == 1:
            yield key


def find_one_image(descriptor: tp.Dict[str, dict]) -> str:
    """Find the key of image data in descriptor."""
    for key, dct in descriptor["data_keys"].items():
        if dct["dtype"] == "array" and len(dct["shape"]) >= 2:
            return key
    raise ValueNotFoundError("No image array found in {}".format(", ".join(descriptor["data_keys"].keys())))


def get_units(data_keys: dict, indeps: typing.Iterable[str]) -> typing.Dict[str, str]:
    """Get the units of variables."""
    return {
        indep: data_keys[indep].get("units", "") for indep in indeps if indep in data_keys
    }


def get_indep_str(data: dict, indep2unit: typing.Dict[str, str]) -> SpecialStr:
    """Get a string of independent variables and their value and their units to export in the file name."""
    stack = []
    for indep, unit in indep2unit.items():
        if indep in data:
            stack.append("{}_{:.2f}{}_".format(indep, data[indep], unit).replace(".", ","))
    return SpecialStr(''.join(stack))
