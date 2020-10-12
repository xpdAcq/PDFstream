import matplotlib.pyplot as plt
import numpy as np
import pytest

import pdfstream.integration.main as integ


@pytest.mark.parametrize(
    "mask, bg_img, kwargs",
    [
        (None, None, {}),
        (
            None,
            'Kapton_img',
            {'bg_scale': 0.001, 'plot_setting': 'OFF', 'img_setting': 'OFF', 'mask_setting': 'OFF'}),
        (
            None,
            None,
            {'mask_setting': {"alpha": 3}, 'plot_setting': 'OFF', 'img_setting': 'OFF'}
        ),
        (
            'mask',
            None,
            {'mask_setting': "OFF", 'plot_setting': 'OFF', 'img_setting': 'OFF'}
        ),
        (
            None,
            None,
            {
                'integ_setting': {'npt': 1024}, 'plot_setting': 'OFF', 'img_setting': 'OFF', 'mask_setting': 'OFF'
            }
        ),
    ]
)
def test_get_chi(test_data, mask, bg_img, kwargs):
    integ.get_chi(test_data['ai'], test_data['Ni_img'].copy(), bg_img=test_data.get(bg_img, None), **kwargs)
    plt.close()


@pytest.mark.parametrize(
    "img, bg_img",
    [
        ("black_img", None),
        ("white_img", "white_img")
    ]
)
def test_get_chi_sanity(test_data, img, bg_img):
    npt = 64
    result = integ.get_chi(
        test_data['ai'],
        test_data.get(img, None).copy(),
        bg_img=test_data.get(bg_img, None),
        mask_setting="OFF",
        integ_setting={'npt': npt},
        plot_setting="OFF",
        img_setting="OFF"
    )
    chi = result[0]
    assert np.array_equal(chi[1], np.zeros(npt))
    plt.close()


def test_avg_imgs(test_data):
    res = integ.avg_imgs([test_data['white_img'], test_data['white_img']], weights=[1, 1])
    assert np.array_equal(res, test_data['white_img'])
