import typing

import pdfstream.io as io
import pdfstream.utils.dct_ops as dct_ops


def query_ai(
    start: typing.Dict[str, typing.Any],
    keys: tuple = ('calibration_md',),
    poni_file: str = None
) -> typing.Dict[str, typing.Any]:
    """Query the azimuthal integrator from the start document.

    If the poni_file is provided, use the poni file instead and ignore the information in start document.

    Parameters
    ----------
    start :
        The start document.

    keys :
        The key chain to find the calibration metadata.

    poni_file :
        If provided, return the azimuthal integrator from the poni file.

    Returns
    -------
    ai :
        The azimuthal integrator.
    """
    if poni_file:
        return io.load_ai_from_poni_file(poni_file)
    calibration_md = dct_ops.get_value(start, keys)
    return io.load_ai_from_calib_result(calibration_md)
