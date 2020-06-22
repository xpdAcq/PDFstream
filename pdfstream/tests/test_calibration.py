from pdfstream.calibration.main import *


def test_calib_pipe(db):
    pdfgetter, recipe = calib_pipe(
        db['ai'], db['Ni_config'], db['Ni_stru'], db['Ni_img'], fit_range=(2., 10., .1)
    )
    assert pdfgetter is not None
    assert recipe is not None
