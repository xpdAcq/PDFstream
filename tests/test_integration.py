import matplotlib.pyplot as plt
import numpy as np

import pdfstream.integration.main as integ


def test_get_chi(db):
    integ.get_chi(db['ai'], db['Ni_img'], db['Kapton_img'], bg_scale=0.04)
    plt.close()


def test_avg_imgs(db):
    res = integ.avg_imgs([db['white_img'], db['white_img']], weights=[1, 1])
    assert np.array_equal(res, db['white_img'])
