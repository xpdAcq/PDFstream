from pathlib import Path

import numpy as np
import pytest
from pkg_resources import resource_filename

import pdfstream.servers.lsq_server as mod
from pdfstream.callbacks.composer import gen_stream

cfg_file = resource_filename("tests", "configs/lsq_server.ini")


@pytest.fixture
def runs():
    x = np.arange(0, 26, 0.1)
    comp0 = gen_stream(
        [{"q": x, "iq": np.sin(x)}],
        {"lsq_type": "component", "sample_name": "c0"}
    )
    comp1 = gen_stream(
        [{"q": x, "iq": np.cos(x)}],
        {"lsq_type": "component", "sample_name": "c1"}
    )
    target = gen_stream(
        [{"q": x, "iq": np.cos(x) + np.sin(x) + np.exp(x / 26)}],
        {"lsq_type": "target", "lsq_comps": ["c0", "c1"], "sample_name": "c2"}
    )
    return comp0, comp1, target


def test_LSQRunRouter(runs, tmpdir):
    config = mod.LSQConfig()
    config.read(cfg_file)
    config.set("EXPORTATION", "directory", str(tmpdir))
    lsq_cb = mod.LSQRunRouter(config)
    for run in runs:
        for name, doc in run:
            lsq_cb(name, doc)
    assert len(tmpdir.listdir()) > 0


def test_make_and_run(tmpdir):
    tmp_ini = Path(tmpdir.join("test.ini"))
    config = mod.LSQServerConfig()
    config.read(cfg_file)
    config.set("EXPORTATION", "directory", str(tmpdir))
    with tmp_ini.open("w") as f:
        config.write(f)
    mod.make_and_run(str(tmp_ini), test_mode=True)
