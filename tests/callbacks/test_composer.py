import pytest

import pdfstream.callbacks.composer as mod


@pytest.fixture
def gen_stream_args(test_data):
    data = {
        "img": test_data['Ni_img'],
        "motor": 0.0,
        "count": 1,
        "is_img": True,
        "name": "image"
    }
    metadata = {"hints": {"dimensions": [(["motor"], "primary")]}}
    return [data], metadata


def test_gen_stream(gen_stream_args):
    stream = mod.gen_stream(*gen_stream_args)
    for name, doc in stream:
        print(name, doc)
