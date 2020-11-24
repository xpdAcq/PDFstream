import numpy as np
import pytest
from diffpy.pdfgetx import PDFConfig

import pdfstream.callbacks.from_start as mod
from pdfstream.data import ni_dspacing_file


def test_query_ai(db_with_dark_and_light):
    db = db_with_dark_and_light
    start = mod.get_start_of_run(db[-1])
    mod.query_ai(start, "calibration_md")


@pytest.mark.parametrize(
    "det_name, shape",
    [
        ("pe1_image", (2048, 2048)),
        pytest.param("pe1_stats1_total", None, marks=pytest.mark.xfail)
    ]
)
def test_get_img_from_run(db_with_dark_and_light, det_name, shape):
    db = db_with_dark_and_light
    img = mod.get_img_from_run(db[-1], det_name)
    assert img.shape == shape


@pytest.mark.parametrize(
    "dk_id_key, shape",
    [
        ("sc_dk_field_uid", (2048, 2048)),
        ("a_key_not_existing", None)
    ]
)
def test_query_dk_img(db_with_dark_and_light, dk_id_key, shape):
    db = db_with_dark_and_light
    start = mod.get_start_of_run(db[-1])
    dk_img = mod.query_dk_img(start, det_name="pe1_image", db=db, dk_id_key=dk_id_key)
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
            ('Ni1.0', None)
        ),
        (
            {'bt_wavelength': 0.16},
            'sample_composition',
            'bt_wavelength',
            ('Ni', 0.16)
        ),
        (
            {'sample_composition': 'C60'},
            'sample_composition',
            'bt_wavelength',
            ('C60', None)
        )
    ]
)
def test_query_bt_info(start, composition_key, wavelength_key, expect):
    config = mod.query_bt_info(
        start,
        composition_key=composition_key,
        wavelength_key=wavelength_key,
        default_composition="Ni"
    )
    pdfconfig = PDFConfig(**config)
    assert (pdfconfig.composition, pdfconfig.wavelength) == expect


def test_query_bg_img(db_with_img_and_bg_img, test_data):
    db = db_with_img_and_bg_img
    run = db[-1]
    bg_img = mod.query_bg_img(
        run.metadata['start'],
        bkgd_sample_name_key="bkgd_sample_name",
        sample_name_key="sample_name",
        det_name="pe1_image",
        db=db,
        dk_id_key="sc_dk_field_uid"
    )
    assert np.array_equal(bg_img, np.ones_like(test_data["Ni_img"]))


@pytest.mark.parametrize(
    "start, expect",
    [
        (
            {"detector": "perkin_elmer", "bt_wavelength": 0.18, "sample_name": "Ni_calib"},
            {"detector": "perkin_elmer", "wavelength": '0.18', "calibrant": str(ni_dspacing_file)}
        )
    ]
)
def test_get_calib_info(start, expect):
    dct = mod.get_calib_info(start, "detector", "bt_wavelength", "sample_name")
    assert dct == expect
