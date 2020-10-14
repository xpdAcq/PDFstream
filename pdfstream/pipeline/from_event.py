"""Get data from event."""
import numpy
import typing


def get_image_from_event(
    event: typing.Dict[str, typing.Any],
    det_name: str
) -> numpy.ndarray:
    """Read the image data from the event.

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
    data: dict = event['data']
    arr = numpy.asarray(data[det_name])
    img = numpy.squeeze(arr)
    if img.ndim != 2:
        raise ValueError("Invalid image dimension. Expect 2 but this is {}".format(img.ndim))
    return img
