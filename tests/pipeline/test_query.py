import numpy as np
import pytest

import pdfstream.pipeline.query as query


def test_query_ai(run0, test_data):
    start = query.get_start_of_run(run0)
    ai = query.query_ai(start)
    print(ai)


@pytest.mark.parametrize(
    "det_name, shape",
    [
        ("pe1_image", (2048, 2048)),
        pytest.param("pe1_stats1_total", None, marks=pytest.mark.xfail)
    ]
)
def test_get_img_from_run(run0, det_name, shape):
    img = query.get_img_from_run(run0, det_name)
    assert img.shape == shape


@pytest.mark.parametrize(
    "dk_id_key, shape",
    [
        ("sc_dk_field_uid", (2048, 2048)),
        ("a_key_not_existing", None)
    ]
)
def test_query_dark(run0, db, dk_id_key, shape):
    dk_start = query.get_start_of_run(run0)
    dk_img = query.query_dark(dk_start, det_name="pe1_image", db=db, dk_id_key=dk_id_key)
    if shape:
        assert isinstance(dk_img, np.ndarray)
        assert dk_img.shape == shape
    else:
        assert dk_img is None
