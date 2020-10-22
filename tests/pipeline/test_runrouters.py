import bluesky.plans as bp
import pytest
import rapidz as rz
from bluesky import RunEngine
from ophyd.sim import hw

import pdfstream.pipeline.runrouters as mod


@pytest.mark.parametrize(
    "metadata, expect",
    [({}, 6), ({"dark_frame": False}, 6), ({"dark_frame": True}, 0)]
)
def test_not_dark_numpy_reg_router(run0, metadata, expect):
    source = rz.Stream()
    lst = source.sink_to_list()
    router = mod.not_dark_numpy_reg_router([lambda *x: source.emit(x[0])])
    RE = RunEngine()
    HW = hw()
    RE.subscribe(router)
    RE(bp.count([HW.img]), **metadata)
    assert len(lst) == expect
