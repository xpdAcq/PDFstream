"""Get data from the start and database."""
import itertools
import typing

import numpy
from databroker.core import BlueskyRunFromGenerator
from databroker.v2 import Broker
from numpy import ndarray

import pdfstream.io as io
from pdfstream.data import ni_dspacing_file


def query_ai(
    start: typing.Dict[str, typing.Any],
    calibration_md_key: str,
) -> typing.Union[None, typing.Dict[str, typing.Any]]:
    """Query the azimuthal integrator from the start document.

    If the poni_file is provided, use the poni file instead and ignore the information in start document.

    Parameters
    ----------
    start :
        The start document.

    calibration_md_key :
        The key chain to find the calibration metadata.

    Returns
    -------
    ai :
        The azimuthal integrator.
    """
    if calibration_md_key not in start:
        raise ValueError("Missing key {} in start document.".format(calibration_md_key))
    return io.load_ai_from_calib_result(start[calibration_md_key])


def query_bg_img(
    start: typing.Dict[str, typing.Any],
    bkgd_sample_name_key: str,
    sample_name_key: str,
    det_name: str,
    db: Broker = None,
    dk_id_key: str = None
) -> typing.Union[ndarray, None]:
    """Find background image from database according to the start document of a run.

    The function will find the background run id in the start and query this run in database. Then, it read
    the image data from the run. If dark image id is also provided, it will subtract the dark image from
    the background image. It assumes that the image is a single shot. If no background image id info in start
    document, return None.

    Parameters
    ----------
    start :
        The start document of the measurement run. It may contain the id of the background run.

    bkgd_sample_name_key :
        The key of the sample of background.

    sample_name_key :
        The key of the sample name.

    det_name :
        The name in the background image data in the xarray of the run.

    db :
        The database that contains the background image run.

    dk_id_key :
        The key of dark image id in the start document of background image run.

    Returns
    -------
    bg_img :
        The background image either dark subtracted or raw. If not found, None.
    """
    if db is None:
        return None
    sample_name = start.get(bkgd_sample_name_key)
    result = list(db.search({sample_name_key: sample_name}))
    if len(result) == 0:
        return None
    bg_run = db[result[-1]]
    img = get_img_from_run(bg_run, det_name=det_name)
    bg_start = get_start_of_run(bg_run)
    dk_img = query_dk_img(bg_start, det_name=det_name, db=db, dk_id_key=dk_id_key) if dk_id_key else None
    return numpy.subtract(img, dk_img) if dk_img is not None else img


def query_dk_img(
    start: typing.Dict[str, typing.Any],
    det_name: str,
    db: Broker = None,
    dk_id_key: str = None
) -> typing.Union[ndarray, None]:
    """Find the dark image according to the start document of a run.

    The function will find the dark id in the start document and search the dark run in database and read the
    image from the run. It assumes that the image is a single shot. If no dark id info in the start document,
    return None.

    Parameters
    ----------
    start :
        The start document of a run.

    det_name :
        The name in the background image data in the xarray of the run.

    db :
        The database that contains the background image run.

    dk_id_key :
        The key of dark image id in the start document of background image run.

    Returns
    -------
    dk_img :
        The raw dark image. If not found, None.
    """
    dk_run = get_dk_run(start, db, dk_id_key)
    if dk_run is None:
        return None
    return get_img_from_run(dk_run, det_name)


def get_dk_run(start: dict, db: Broker, dk_id_key: str) -> typing.Union[BlueskyRunFromGenerator, None]:
    """Get the dark image run id. If not found, return None."""
    if db and dk_id_key and dk_id_key in start:
        dk_id = start[dk_id_key]
        return db[dk_id]
    return None


def get_img_from_run(run: BlueskyRunFromGenerator, det_name: str) -> ndarray:
    """Read a single image of a detector from a run (databroker v2)."""
    ds = run.primary.read()
    img: ndarray = ds[det_name].values
    # remove all single dimensions
    img = numpy.squeeze(img)
    if img.ndim != 2:
        raise ValueError("Invalid number of dimension for an image: {}. Expect 2.".format(img.ndim))
    return img


def get_start_of_run(run: BlueskyRunFromGenerator):
    """Read the start document of a run (databroker v2)."""
    return run.metadata['start']


def query_bt_info(
    start: typing.Dict[str, typing.Any],
    composition_key: str,
    wavelength_key: str,
    default_composition: str = "Ni"
) -> dict:
    """Query the necessary information for the PDFGetter."""
    if composition_key in start:
        composition = start[composition_key]
        if isinstance(composition, dict):
            composition_str = "".join(["{}{}".format(k, v) for k, v in composition.items()])
        elif isinstance(composition, str):
            composition_str = composition
        else:
            raise ValueError("Cannot parse composition: {}".format(type(composition)))
    else:
        composition_str = default_composition
    if wavelength_key in start:
        wavelength = float(start[wavelength_key])
    else:
        wavelength = None
    return {
        "composition": composition_str,
        "wavelength": wavelength
    }


def get_indeps(start: dict, exclude: set = frozenset()) -> set:
    """Get independent variables from the hints in start."""
    return set(
        itertools.chain.from_iterable(
            [n for n, s in start.get("hints", {}).get("dimensions", [])]
        )
    ) - exclude


def get_calib_info(
    start: typing.Dict[str, typing.Any],
    detector_key: str,
    wavelength_key: str,
    calibrant_key: str
) -> typing.Dict[str, str]:
    """Get the information for pyfail calib2 gui in the start. If no such key, return empty string."""
    calibrant = str(start.get(calibrant_key, ""))
    # a special case for xpdacq
    calibrant = str(ni_dspacing_file) if calibrant in ("Ni_calib", "Ni") else calibrant
    return {
        "detector": str(start.get(detector_key, "")),
        "wavelength": str(start.get(wavelength_key, "")),
        "calibrant": calibrant
    }
