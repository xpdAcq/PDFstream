import matplotlib.pyplot as plt
import pytest
import rapidz as rz
from bluesky.callbacks.broker import LiveImage
from xpdview.callbacks import LiveWaterfall

import pdfstream.pipeline.callbacks as mod
from pdfstream.pipeline.errors import ValueNotFoundError
from pdfstream.pipeline.preprocess import basic_doc_stream


def see_image(live_image: LiveImage):
    fig = live_image.cs._fig
    fig.show()
    plt.close(fig)
    return


def see_wafterfall(live_waterfall: LiveWaterfall):
    for waterfall in live_waterfall.wfs.values():
        waterfall.fig.show()
        plt.close(waterfall.fig)
    return


def test_StripDepVar(run0):
    cb = mod.StripDepVar()
    for name, doc in basic_doc_stream(run0):
        cb(name, doc)
        print(name, doc)


@pytest.mark.parametrize(
    "dk_id_key",
    [None, "sc_dk_field_uid"]
)
def test_DarkSubtraction(run0, dk_id_key):
    cb = mod.DarkSubtraction(db_name="example", dk_id_key=dk_id_key)
    vis = LiveImage("dk_sub_img")
    for name, doc in basic_doc_stream(run0):
        name, doc = cb(name, doc)
        vis(name, doc)
        print(name, doc)
    see_image(vis)


@pytest.mark.parametrize(
    "calibration_md_key",
    ["calibration_md", None]
)
def test_AutoMasking(run0, calibration_md_key):
    cb0 = mod.DarkSubtraction(db_name="example", dk_id_key="sc_dk_field_uid")
    cb = mod.AutoMasking(calibration_md_key=calibration_md_key, mask_setting={"alpha": 2})
    vis = LiveImage("masked_img")
    for name, doc in basic_doc_stream(run0):
        name, doc = cb0(name, doc)
        name, doc = cb(name, doc)
        vis(name, doc)
    see_image(vis)


@pytest.mark.parametrize(
    "calibration_md_key",
    ["calibration_md", pytest.param(None, marks=pytest.mark.xfail(raises=ValueNotFoundError))]
)
def test_AzimuthalIntegration(run0, calibration_md_key):
    cb0 = mod.DarkSubtraction(db_name="example", dk_id_key="sc_dk_field_uid")
    cb = mod.AzimuthalIntegration(calibration_md_key=calibration_md_key, integ_setting={}, pyfai_unit="q_A^-1")
    vis = LiveWaterfall()
    for name, doc in basic_doc_stream(run0):
        name, doc = cb0(name, doc)
        name, doc = cb(name, doc)
        vis(name, doc)
    see_wafterfall(vis)


@pytest.mark.parametrize(
    "pyfai_unit",
    ["q_A^-1", "2th_rad", pytest.param("r_mm", marks=pytest.mark.xfail(raises=KeyError))]
)
def test_TransformIQtoFQ(run0, pyfai_unit):
    cb0 = mod.DarkSubtraction(db_name="example", dk_id_key="sc_dk_field_uid")
    cb1 = mod.AzimuthalIntegration(calibration_md_key="calibration_md", integ_setting={}, pyfai_unit=pyfai_unit)
    cb = mod.TransformIQtoFQ(composition_key="sample_composition", wavelength_key="bt_wavelength",
                             pyfai_unit=pyfai_unit, trans_setting={"qmaxinst": 24, "qmax": 22})
    vis = LiveWaterfall()
    for name, doc in basic_doc_stream(run0):
        name, doc = cb0(name, doc)
        name, doc = cb1(name, doc)
        name, doc = cb(name, doc)
        vis(name, doc)
    see_wafterfall(vis)


def test_TransformFQtoGr(run0):
    pyfai_unit = "q_A^-1"
    cb0 = mod.DarkSubtraction(db_name="example", dk_id_key="sc_dk_field_uid")
    cb1 = mod.AzimuthalIntegration(calibration_md_key="calibration_md", integ_setting={}, pyfai_unit=pyfai_unit)
    cb2 = mod.TransformIQtoFQ(composition_key="sample_composition", wavelength_key="bt_wavelength",
                              pyfai_unit=pyfai_unit, trans_setting={"qmaxinst": 24, "qmax": 22})
    cb = mod.TransformFQtoGr(grid_config={"rmin": 0., "rmax": 20, "rstep": 0.01})
    vis = LiveWaterfall()
    for name, doc in basic_doc_stream(run0):
        name, doc = cb0(name, doc)
        name, doc = cb1(name, doc)
        name, doc = cb2(name, doc)
        name, doc = cb(name, doc)
        vis(name, doc)
    see_wafterfall(vis)


@pytest.mark.parametrize(
    "filters, unpack, expect",
    [
        (
            frozenset([
                "start", "descriptor", "datum", "datum_page", "event", "event_page", "stop"
            ]),
            False,
            ["start", "descriptor", "datum_page", "event_page", "stop"]
        ),
        (
            frozenset([
                "start", "descriptor", "datum", "datum_page", "event", "event_page", "stop"
            ]),
            True,
            ["start", "descriptor", "datum", "event", "stop"]
        ),
        (
            frozenset([
                "start", "descriptor", "event", "event_page", "stop"
            ]),
            True,
            ["start", "descriptor", "event", "stop"]
        )
    ]
)
def test_AnalysisCallback(run0, filters, unpack, expect):
    source = rz.Stream()
    node = rz.starmap(source, lambda *x: x[0])
    lst = node.sink_to_list()
    cb = mod.AnalysisCallback(source, filters=filters, unpack=unpack)
    for name, doc in run0.canonical(fill="no"):
        cb(name, doc)
    assert lst == expect
