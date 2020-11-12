import pytest

import pdfstream.callbacks.from_descriptor as mod

DCT0 = {'camera_image': {'dtype': 'number',
                         'shape': [512, 512],
                         'source': 'PV:...'}}

DCT1 = {'camera_image': {'dtype': 'array',
                         'shape': [],
                         'source': 'PV:...'}}

DCT2 = {'camera_image': {'dtype': 'number',
                         'shape': [512],
                         'source': 'PV:...'}}

DCT3 = {'camera_image': {'dtype': 'boolean',
                         'shape': [512, 512],
                         'source': 'PV:...'}}


@pytest.mark.parametrize(
    "dct, expect",
    [
        pytest.param(DCT1, 'camera_image'),
        pytest.param(DCT1, 'camera_image'),
        pytest.param(DCT2, 'camera_image', marks=pytest.mark.xfail),
        pytest.param(DCT3, 'camera_image', marks=pytest.mark.xfail)
    ]
)
def test_find_one_2darray(dct, expect):
    outcome = mod.find_one_array(dct)
    assert outcome == expect
