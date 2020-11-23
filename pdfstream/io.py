"""The input / output functions related to file system."""
from pathlib import Path
from typing import Dict, Any

import fabio
import pyFAI
import yaml
from numpy import ndarray

from pdfstream.vend.loaddata import load_data


def load_ai_from_poni_file(poni_file: str) -> pyFAI.AzimuthalIntegrator:
    """Initiate the AzimuthalIntegrator using poni file."""
    ai = pyFAI.load(poni_file)
    return ai


def load_ai_from_calib_result(calib_result: dict) -> pyFAI.AzimuthalIntegrator:
    """Initiate the AzimuthalIntegrator using calibration information."""
    ai = pyFAI.azimuthalIntegrator.AzimuthalIntegrator()
    # different from poni file, set_config only accepts dictionary of lowercase keys
    _calib_result = _lower_key(calib_result)
    # the pyFAI only accept strings so the None should be parsed to a string
    _calib_result = _str_none(_calib_result)
    # the old version of poni uses dist intead of distance and the new version only recognize "distance"
    if ("dist" in _calib_result) and "distance" not in _calib_result:
        _calib_result["distance"] = _calib_result["dist"]
    ai.set_config(_calib_result)
    return ai


def load_img(img_file: str) -> ndarray:
    """Load the img data from the img_file."""
    img = fabio.open(img_file).data
    return img


def write_img(filepath: str, img: ndarray, template: str) -> None:
    """Write out the image data as the same type of the template file."""
    temp_img = fabio.open(template)
    temp_img.data = img
    temp_img.save(filepath)
    return


def load_array(data_file: str, minrows=10, **kwargs) -> ndarray:
    """Load data columns from the .txt file and turn columns to rows and return the numpy array."""
    return load_data(data_file, minrows=minrows, **kwargs).T


def load_dict_from_poni(poni_file: str) -> dict:
    """Turn the poni file to pyFAI readable dictionary."""
    with Path(poni_file).open('r') as f:
        geometry = yaml.safe_load(f)
    return _lower_key(geometry)


def _lower_key(dct: Dict[str, Any]) -> Dict[str, Any]:
    """Return dictionary with all keys in lower case."""
    return {key.lower(): value for key, value in dct.items()}


def _str_none(dct: Dict[str, Any]) -> Dict[str, Any]:
    """Make all the None value to string 'none'."""
    return {key: "none" if value is None else value for key, value in dct.items()}
