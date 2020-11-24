from pathlib import Path

import pytest
from pkg_resources import resource_filename

import pdfstream.servers
import pdfstream.servers.base as mod

fn = Path(resource_filename("tests", "configs"))


@pytest.mark.parametrize(
    "name", ["xpd", "lsq", pytest.param("unknown", marks=pytest.mark.xfail(raises=FileNotFoundError))]
)
def test_find_cfg_file(name):
    mod.find_cfg_file(fn, name)


def test_StartStopCallback(simple_stream):
    cb = pdfstream.servers.base.StartStopCallback()
    for name, doc in simple_stream:
        cb(name, doc)
