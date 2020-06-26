import matplotlib.pyplot as plt
import numpy as np

import pdfstream.integration.main as integ


def test_get_chi(db):
    chi = integ.get_chi(db['ai'], db['black_img'], db['black_img'])
    assert chi.shape == (2, 1480)
    assert np.array_equal(chi[1], np.zeros(1480))
    plt.close()


def test_avg_imgs(db):
    res = integ.avg_imgs([db['white_img'], db['white_img']], weights=[1, 1])
    assert np.array_equal(res, db['white_img'])
