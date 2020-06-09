import numpy as np

import pdfstream.integration as integ


def test_main(db):
    chi = integ.main(db['ai'], db['black_img'], db['black_img'])
    npt = integ._INTEG_SETTING['npt']
    assert chi.shape == (2, npt)
    assert np.array_equal(chi[1], np.zeros(npt))
