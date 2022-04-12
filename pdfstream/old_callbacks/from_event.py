"""Get data from event."""
import typing

import numpy
from numpy import ndarray


def get_image_from_event(
    event: typing.Dict[str, typing.Any],
    det_name: str
) -> numpy.ndarray:
    """Read the image data from the event. It will be transferred to a 2D numpy array.

    Parameters
    ----------
    event :
        The event document.

    det_name :
        The name of the key to the image. Usually, the detector name.

    Returns
    -------
    img :
        The two dimensional array of image.
    """
    data = event['data'][det_name]
    return get_average_frame(data)


def get_average_frame(
    arr: typing.Union[list, ndarray]
) -> ndarray:
    """Get the average frame from a list of frames."""
    img = numpy.asarray(arr)
    if img.ndim < 2:
        raise ValueError("Invalid image dimension {}. A image should have at least 2 dimensions.".format(img.ndim))
    if img.ndim > 2:
        img = img.mean(axis=tuple(range(img.ndim - 2)))
    return img
