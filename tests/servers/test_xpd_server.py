import os
import signal
import time
from multiprocessing import Process
from pathlib import Path
from threading import Thread

import bluesky.plans as bp
import pytest
from bluesky import RunEngine
from bluesky.callbacks.zmq import Publisher
from databroker.core import BlueskyRun
from ophyd.sim import hw
from pkg_resources import resource_filename

import pdfstream.servers.xpd_server as mod

fn = resource_filename("tests", "configs/xpd.ini")


def interrupt(delay: float) -> None:
    """Keyboard interrupt after delay. Used in testing servers."""
    time.sleep(delay)
    print("Keyboard interrupt ...")
    os.kill(os.getpid(), signal.SIGINT)


def experiment(run: BlueskyRun, delay: float, address: str, prefix: bytes = b''):
    """Send docs to proxy. Used in testing servers."""
    time.sleep(delay)
    publisher = Publisher(address, prefix=prefix)
    for name, doc in run.canonical(fill="yes"):
        publisher(name, doc)
    return


def experiment1(delay: float, address: str, prefix: bytes):
    time.sleep(delay)
    HW = hw()
    RE = RunEngine()
    RE.subscribe(Publisher(address, prefix=prefix))
    RE(bp.count([HW.img]))


def experiment2(delay: float, address: str, prefix: bytes):
    time.sleep(delay)
    HW = hw()
    RE = RunEngine()
    RE.subscribe(Publisher(address, prefix=prefix))
    RE(bp.scan([HW.img], HW.motor, 0, 3, 3))


def test_XPDServerConfig():
    config = mod.XPDServerConfig()
    config.read(fn)
    assert len(config.sections()) > 0


def test_make_and_run(run0, proxy, tmpdir):
    process = Process(target=experiment, args=(run0, 2, proxy[0], b'raw'), daemon=True)
    thread = Thread(target=interrupt, args=(10,))
    thread.start()
    process.start()
    mod.make_and_run(fn, test_tiff_base=str(tmpdir))
    thread.join()
    process.join()
    folder = Path(str(tmpdir))
    assert len(list(folder.rglob("*.tiff"))) == 2
    assert len(list(folder.rglob("*.csv"))) == 1
    assert len(list(folder.rglob("*.json"))) == 1


@pytest.mark.parametrize(
    "exp_func, num_tiff, num_csv, num_json",
    [
        (experiment1, 1, 0, 1),
        (experiment2, 3, 1, 1)
    ]
)
def test_make_and_run_for_experiments(proxy, tmpdir, exp_func, num_tiff, num_csv, num_json):
    process = Process(target=exp_func, args=(1, proxy[0], b'raw'), daemon=True)
    thread = Thread(target=interrupt, args=(4,))
    thread.start()
    process.start()
    mod.make_and_run(fn, test_tiff_base=str(tmpdir))
    thread.join()
    process.join()
    folder = Path(str(tmpdir))
    assert len(list(folder.rglob("*.tiff"))) == num_tiff
    assert len(list(folder.rglob("*.csv"))) == num_csv
    assert len(list(folder.rglob("*.json"))) == num_json
