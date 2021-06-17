"""Get data from the start and database."""
import itertools
import typing

from databroker import Header
from databroker.v1 import Broker
from numpy import ndarray

import pdfstream.io as io
from pdfstream.data import ni_dspacing_file
from pdfstream.errors import ValueNotFoundError


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
        raise ValueNotFoundError("Missing key {} in start document.".format(calibration_md_key))
    return io.load_ai_from_calib_result(start[calibration_md_key])


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
    dk_run = get_dk_run_v1(start, db, dk_id_key)
    return get_img_from_run_v1(dk_run, det_name)


def get_dk_run_v1(start: dict, db: Broker, dk_id_key: str) -> typing.Union[Header]:
    """Get the dark image run id. If not found, return None."""
    if not db:
        raise ValueNotFoundError("db is None.")
    if not dk_id_key:
        raise ValueNotFoundError("dk_id_key is None.")
    if dk_id_key not in start:
        raise ValueNotFoundError("No such a key in start: {}".format(dk_id_key))
    dk_id = start[dk_id_key]
    try:
        return db[dk_id]
    except KeyError:
        raise ValueNotFoundError("No such a run in db: {}".format(dk_id))


def get_img_from_run_v1(run: Header, det_name: str) -> ndarray:
    """Read a single image of a detector from a run (databroker v2)."""
    if det_name not in run.fields():
        raise ValueNotFoundError("No such a det_name '{}' in run '{}'".format(det_name, run.uid))
    try:
        img = mean(run.data(det_name))
    except StopIteration:
        raise ValueNotFoundError("No images data for '{}' in run '{}'".format(det_name, run.uid))
    if img.ndim > 2:
        img = img.mean(axis=tuple(range(img.ndim - 2)))
    return img


def mean(images: typing.Iterable[ndarray]) -> ndarray:
    """Calculate mean of an iterator of numpy array."""
    image_iter = iter(images)
    avg_image = next(image_iter)
    count = 1
    for image in image_iter:
        avg_image += image
    return avg_image / count


def get_start_of_run_v1(run: Header):
    """Read the start document of a run (databroker v2)."""
    return run.start


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
            io.server_message(
                "Cannot parse composition '{}'. Use default '{}'".format(composition, default_composition))
            composition_str = default_composition
    else:
        io.server_message("'{}' is not in start. Use default '{}'".format(composition_key, default_composition))
        composition_str = default_composition
    if wavelength_key in start:
        wavelength = float(start[wavelength_key])
    else:
        io.server_message("'{}' is not in start. Use None.".format(wavelength_key))
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
    """Get the information for pyfail calib2 gui in the start. If no such key, return default."""
    calibrant = str(start.get(calibrant_key, ""))
    # a special case for xpdacq
    calibrant = str(ni_dspacing_file) if "Ni" in calibrant or not calibrant else calibrant
    return {
        "detector": str(start.get(detector_key, "")),
        "wavelength": str(start.get(wavelength_key, "")),
        "calibrant": calibrant
    }
