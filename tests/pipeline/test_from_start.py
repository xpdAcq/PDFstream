import numpy as np
import pytest
from diffpy.pdfgetx import PDFConfig

import pdfstream.pipeline.from_start as mod


def test_query_ai(run0, test_data):
    start = mod.get_start_of_run(run0)
    ai = mod.query_ai(start, "calibration_md")
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
def test_query_dk_img(run0, db, dk_id_key, shape):
    dk_start = mod.get_start_of_run(run0)
    dk_img = mod.query_dk_img(dk_start, det_name="pe1_image", db=db, dk_id_key=dk_id_key)
    if shape:
        assert isinstance(dk_img, np.ndarray)
        assert dk_img.shape == shape
    else:
        assert dk_img is None


@pytest.mark.parametrize(
    "start, composition_key, wavelength_key, expect",
    [
        (
            {'sample_composition': {'Ni': 1.0}},
            'sample_composition',
            'bt_wavelength',
            ({'Ni': 1.0}, None)
        ),
        (
            {'bt_wavelength': 0.16},
            'sample_composition',
            'bt_wavelength',
            ('', 0.16)
        )
    ]
)
def test_query_bt_info(start, composition_key, wavelength_key, expect):
    config = mod.query_bt_info(start, composition_key=composition_key, wavelength_key=wavelength_key)
    pdfconfig = PDFConfig(**config)
    assert (pdfconfig.composition, pdfconfig.wavelength) == expect
