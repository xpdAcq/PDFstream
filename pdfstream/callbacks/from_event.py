"""Get data from event."""
import numpy
import typing
from numpy import ndarray

from pdfstream.errors import ValueNotFoundError


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


def find_one_image(event: typing.Dict[str, dict]) -> typing.Tuple[str, ndarray]:
    """Find an array that can be squeezed to 2d array in the event data."""
    for key, data in event["data"].items():
        if numpy.ndim(data) >= 2:
            img = numpy.squeeze(numpy.asarray(data))
            if img.ndim == 2:
                return key, img
    raise ValueNotFoundError("Image not found in event.")


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


def get_masked_array_from_event(
    event: typing.Dict[str, typing.Any],
    det_name: str
):
    """Get a masked image from the event. The return is the numpy masked array."""
    data = event['data'][det_name]
    data = numpy.ma.asarray(data)
    data = numpy.ma.squeeze(data)
    return data


def get_array_from_event(event: typing.Dict[str, typing.Any], data_key: str):
    """Get a certain dimension numpy array form the event. If the input is a list, convert it to numpy array."""
    data = event["data"][data_key]
    data = numpy.asarray(data)
    data = numpy.squeeze(data)
    return data
