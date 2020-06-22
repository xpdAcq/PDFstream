from pdfstream.calibration.main import *


def test_calib_pipe(db):
    calib_pipe(
        db['ai'], db['Ni_img'], db['Ni_config'], db['Ni_stru'], fit_range=(2., 10., .1)
    )
