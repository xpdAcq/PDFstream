import numpy as np

import pdfstream.average as avg


def test_main(db):
    res = avg.main([db['white_img'], db['white_img']], weights=[1, 1])
    assert np.array_equal(res, db['white_img'])
