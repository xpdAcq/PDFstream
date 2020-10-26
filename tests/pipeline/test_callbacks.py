import pytest

import pdfstream.pipeline.callbacks as mod
from pdfstream.pipeline.errors import ValueNotFoundError
from pdfstream.pipeline.preprocess import basic_doc_stream


def test_StripDepVar(run0):
    cb = mod.StripDepVar()
    for name, doc in basic_doc_stream(run0):
        cb(name, doc)


@pytest.mark.parametrize(
    "dk_id_key",
    [None, "sc_dk_field_uid"]
)
def test_DarkSubtraction(run0, dk_id_key):
    cb = mod.DarkSubtraction(db_name="example", dk_id_key=dk_id_key)
    for name, doc in basic_doc_stream(run0):
        cb(name, doc)


@pytest.mark.parametrize(
    "calibration_md_key",
    ["calibration_md", None]
)
def test_AutoMasking(run0, calibration_md_key):
    cb0 = mod.DarkSubtraction(db_name="example", dk_id_key="sc_dk_field_uid")
    cb = mod.AutoMasking(calibration_md_key=calibration_md_key, mask_setting={"alpha": 2})
    for name, doc in basic_doc_stream(run0):
        name, doc = cb0(name, doc)
        cb(name, doc)


@pytest.mark.parametrize(
    "calibration_md_key",
    ["calibration_md", pytest.param(None, marks=pytest.mark.xfail(raises=ValueNotFoundError))]
)
def test_AzimuthalIntegration(run0, calibration_md_key):
    cb0 = mod.DarkSubtraction(db_name="example", dk_id_key="sc_dk_field_uid")
    cb = mod.AzimuthalIntegration(calibration_md_key=calibration_md_key, integ_setting={}, pyfai_unit="q_A^-1")
    for name, doc in basic_doc_stream(run0):
        name, doc = cb0(name, doc)
        cb(name, doc)


@pytest.mark.parametrize(
    "pyfai_unit",
    ["q_A^-1", "2th_rad", pytest.param("r_mm", marks=pytest.mark.xfail(raises=KeyError))]
)
def test_TransformIQtoFQ(run0, pyfai_unit):
    cb0 = mod.DarkSubtraction(db_name="example", dk_id_key="sc_dk_field_uid")
    cb1 = mod.AzimuthalIntegration(calibration_md_key="calibration_md", integ_setting={}, pyfai_unit=pyfai_unit)
    cb = mod.TransformIQtoFQ(composition_key="sample_composition", wavelength_key="bt_wavelength",
                             pyfai_unit=pyfai_unit, trans_setting={"qmaxinst": 24, "qmax": 22})
    for name, doc in basic_doc_stream(run0):
        name, doc = cb0(name, doc)
        name, doc = cb1(name, doc)
        cb(name, doc)


def test_TransformFQtoGr(run0):
    pyfai_unit = "q_A^-1"
    cb0 = mod.DarkSubtraction(db_name="example", dk_id_key="sc_dk_field_uid")
    cb1 = mod.AzimuthalIntegration(calibration_md_key="calibration_md", integ_setting={}, pyfai_unit=pyfai_unit)
    cb2 = mod.TransformIQtoFQ(composition_key="sample_composition", wavelength_key="bt_wavelength",
                              pyfai_unit=pyfai_unit, trans_setting={"qmaxinst": 24, "qmax": 22})
    cb = mod.TransformFQtoGr(grid_config={"rmin": 0., "rmax": 20, "rstep": 0.01})
    for name, doc in basic_doc_stream(run0):
        name, doc = cb0(name, doc)
        name, doc = cb1(name, doc)
        name, doc = cb2(name, doc)
        cb(name, doc)
