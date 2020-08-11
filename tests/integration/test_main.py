import matplotlib.pyplot as plt
import numpy as np
import pytest

import pdfstream.integration.main as integ


@pytest.mark.parametrize(
    "bg_img_key,kwargs",
    [
        (None, {}),
        ('Kapton_img', {}),
        ('Kapton_img', {'bg_scale': 0.001}),
        ('Kapton_img', {'bg_scale': 0.001, 'mask_setting': "OFF"}),
        ('Kapton_img', {'bg_scale': 0.001, 'mask_setting': {"alpha": 3}}),
        ('Kapton_img', {'bg_scale': 0.001, 'integ_setting': {'npt': 1024}}),
    ]
)
def test_get_chi(db, bg_img_key, kwargs):
    integ.get_chi(db['ai'], db['Ni_img'], bg_img=db.get(bg_img_key, None), **kwargs)
    plt.close()


def test_avg_imgs(db):
    res = integ.avg_imgs([db['white_img'], db['white_img']], weights=[1, 1])
    assert np.array_equal(res, db['white_img'])
