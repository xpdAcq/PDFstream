import typing

import numpy
from databroker import Broker
from databroker.core import BlueskyRunFromGenerator
from numpy import ndarray

import pdfstream.io as io
import pdfstream.utils.dct_ops as dct_ops


def query_ai(
    start: typing.Dict[str, typing.Any],
    keys: tuple = ('calibration_md',),
) -> typing.Dict[str, typing.Any]:
    """Query the azimuthal integrator from the start document.

    If the poni_file is provided, use the poni file instead and ignore the information in start document.

    Parameters
    ----------
    start :
        The start document.

    keys :
        The key chain to find the calibration metadata.

    Returns
    -------
    ai :
        The azimuthal integrator.
    """
    calibration_md = dct_ops.get_value(start, keys)
    return io.load_ai_from_calib_result(calibration_md)


def query_bg_img(
    start: typing.Dict[str, typing.Any],
    bg_id_key: str,
    det_name: str,
    db: Broker,
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

    bg_id_key :
        The key of the id of the background image run.

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
    if bg_id_key not in start:
        return None
    bg_run: BlueskyRunFromGenerator = db[bg_id_key]
    img = get_img_from_run(bg_run, det_name=det_name)
    bg_start = get_start_of_run(bg_run)
    dk_img = query_dk_img(bg_start, det_name=det_name, db=db, dk_id_key=dk_id_key) if dk_id_key else None
    return numpy.subtract(img, dk_img) if dk_img is not None else img


def query_dk_img(
    start: typing.Dict[str, typing.Any],
    det_name: str,
    db: Broker,
    dk_id_key: str
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
    if dk_id_key not in start:
        return None
    dk_id = start[dk_id_key]
    dk_run = db[dk_id]
    return get_img_from_run(dk_run, det_name)


def get_img_from_run(run: BlueskyRunFromGenerator, det_name: str) -> ndarray:
    """Read a single image of a detector from a run (databroker v2)."""
    ds = run.primary.read()
    img: ndarray = ds[det_name].values
    # remove all single dimensions
    img = numpy.squeeze(img)
    if img.ndim != 2:
        raise ValueError(
            "Invalid number of dimension for an image: {}. Expect 2.".format(img.ndim)
        )
    return img


def get_start_of_run(run: BlueskyRunFromGenerator):
    """Read the start document of a run (databroker v2)."""
    return run.metadata['start']


def query_config(start: typing.Dict[str, typing.Any], composition_key: str):
    """Query the necessary information for the PDFGetter."""
    config = {}
    if composition_key in start:
        config.update({"composition": start[composition_key]})
    return config
