import bluesky.plans as bp
import pytest
from bluesky import RunEngine
from databroker import catalog
from ophyd.sim import hw
from rapidz import Stream

import pdfstream.pipeline.analysis as mod


@pytest.fixture
def stream_config():
    return {
        "calibration_md_key": "calibration_md",
        "det_name": "pe1_image",
        "bg_id_key": None,
        "dk_id_key": "sc_dk_field_uid",
        "composition_key": "sample_composition",
        "wavelength_key": "bt_wavelength",
        "bg_scale": 1.,
        "mask_setting": {},
        "integ_setting": {},
        "pdf_setting": {"composition": "Ni"}
    }


@pytest.mark.parametrize(
    "metadata, expect",
    [({}, 4), ({"dark_frame": False}, 4), ({"dark_frame": True}, 0)]
)
def test_analysis_router(metadata, expect):
    source = Stream()
    lst = source.sink_to_list()
    RE = RunEngine()
    HW = hw()
    router = mod.analysis_router([source])
    RE.subscribe(router)
    RE(bp.count([HW.det]), **metadata)
    assert len(lst) == expect


def test_streaming_process_img_to_pdf(stream_config, run0):
    db = catalog["example"]
    nodes = mod.streaming_process_img_to_pdf(stream_config, test_db=db)
    source = nodes["source"]
    lst = nodes["aligned G(r) doc"].sink_to_list()
    nodes["aligned G(r) doc"].sink(print)
    for doc in run0.canonical(fill="yes"):
        source.emit(doc)
    assert len(lst) == 4
