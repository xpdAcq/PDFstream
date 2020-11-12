import numpy
import pytest

import pdfstream.callbacks.from_event as mod

EVENT0 = {
    'time': [0.0],
    'uid': ['6a7a00e2-2a64-4284-9d67-e499ab682eea'],
    'seq_num': [1],
    'descriptor': '7711ee16-4b89-483b-9e96-94eb661cd4ee',
    'filled': {'pe1_image': ['d82442a7-6691-48bc-9c09-ae1c30e0aee4/0']},
    'data': {
        'pe1_image': [numpy.ones((3, 3))],
        'pe1_stats1_total': [9.0]
    }
}


@pytest.mark.parametrize(
    "event, det_name, expect",
    [
        (EVENT0, "pe1_image", numpy.ones((3, 3))),
        pytest.param(EVENT0, "pe1_stats1_total", None, marks=pytest.mark.xfail)
    ]
)
def test_get_image_from_event(event, det_name, expect):
    img = mod.get_image_from_event(event, det_name=det_name)
    assert numpy.array_equal(img, expect)
