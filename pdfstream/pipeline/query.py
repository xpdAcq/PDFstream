import typing

import pdfstream.io as io
import pdfstream.utils.dct_ops as dct_ops


def query_ai(
    start: typing.Dict[str, typing.Any],
    keys: ('calibration_md',),
    poni_file: str = None
) -> typing.Dict[str, typing.Any]:
    if poni_file:
        return io.load_ai_from_poni_file(poni_file)
    calibration_md = dct_ops.get_value(start, keys)
    return io.load_ai_from_calib_result(calibration_md)
