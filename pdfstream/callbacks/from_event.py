"""Get data from event."""
import typing

import numpy
from numpy import ndarray


def get_image_from_event(
    event: typing.Dict[str, typing.Any],
    det_name: str
) -> numpy.ndarray:
    """Read the image data from the event. It will be transferred to a numpy array.

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
    return squeeze_to_image(data)


def squeeze_to_image(
    arr: typing.Union[list, ndarray],
    ndim: int = 2
) -> ndarray:
    """Squeez the array to a 2d image array."""
    arr1 = numpy.asarray(arr)
    img = numpy.squeeze(arr1)
    if img.ndim != ndim:
        raise ValueError("Invalid image dimension. Expect {} but this is {}".format(ndim, img.ndim))
    return img
