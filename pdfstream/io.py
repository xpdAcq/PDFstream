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
    ai = pyFAI.AzimuthalIntegrator()
    ai.set_config(calib_result)
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
