import numpy as np
import pytest
from diffpy.pdfgetx import PDFConfig

import pdfstream.pipeline.from_start as mod


def test_query_ai(run0, test_data):
    start = mod.get_start_of_run(run0)
    ai = mod.query_ai(start)
    print(ai)


@pytest.mark.parametrize(
    "det_name, shape",
    [
        ("pe1_image", (2048, 2048)),
        pytest.param("pe1_stats1_total", None, marks=pytest.mark.xfail)
    ]
)
def test_get_img_from_run(run0, det_name, shape):
    img = mod.get_img_from_run(run0, det_name)
    assert img.shape == shape


@pytest.mark.parametrize(
    "dk_id_key, shape",
    [
        ("sc_dk_field_uid", (2048, 2048)),
        ("a_key_not_existing", None)
    ]
)
def test_query_dark(run0, db, dk_id_key, shape):
    dk_start = mod.get_start_of_run(run0)
    dk_img = mod.query_dark(dk_start, det_name="pe1_image", db=db, dk_id_key=dk_id_key)
    if shape:
        assert isinstance(dk_img, np.ndarray)
        assert dk_img.shape == shape
    else:
        assert dk_img is None


@pytest.mark.parametrize(
    "args",
    [
        ({'sample_composition': {'Ni': 1.0}}, 'sample_composition')
    ]
)
def test_query_config(args):
    config = mod.query_config(*args)
    PDFConfig(**config)
