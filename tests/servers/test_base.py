from pathlib import Path

import pytest
from pkg_resources import resource_filename

import pdfstream.main
import pdfstream.servers
import pdfstream.servers.base as mod

fn = Path(resource_filename("tests", "configs"))


@pytest.mark.parametrize(
    "name",
    ["xpd_server", "lsq_server", pytest.param("unknown", marks=pytest.mark.xfail(raises=FileNotFoundError))]
)
def test_find_cfg_file(name):
    pdfstream.main.find_cfg_file(str(fn), name)


def test_StartStopCallback(simple_stream):
    cb = pdfstream.servers.base.StartStopCallback()
    for name, doc in simple_stream:
        cb(name, doc)


def test_ServerConfig():
    with pytest.raises(FileNotFoundError):
        config = mod.ServerConfig()
        config.read("A missing file")
