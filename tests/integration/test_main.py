import matplotlib.pyplot as plt
import numpy as np
import pytest

import pdfstream.integration.main as integ


@pytest.mark.parametrize(
    "bg_img_key,kwargs",
    [
        (None, {}),
        ('Kapton_img', {'bg_scale': 0.001, 'plot_setting': 'OFF', 'img_setting': 'OFF', 'mask_setting': 'OFF'}),
        ('Kapton_img', {'mask_setting': {"alpha": 3}, 'plot_setting': 'OFF', 'img_setting': 'OFF'}),
        ('Kapton_img', {
            'integ_setting': {'npt': 1024}, 'plot_setting': 'OFF', 'img_setting': 'OFF', 'mask_setting': 'OFF'
        }),
    ]
)
def test_get_chi(db, bg_img_key, kwargs):
    integ.get_chi(db['ai'], db['Ni_img'], bg_img=db.get(bg_img_key, None), **kwargs)
    plt.close()


def test_avg_imgs(db):
    res = integ.avg_imgs([db['white_img'], db['white_img']], weights=[1, 1])
    assert np.array_equal(res, db['white_img'])
