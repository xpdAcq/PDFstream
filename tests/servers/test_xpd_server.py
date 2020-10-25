import os
import signal
import time
from multiprocessing import Process
from threading import Thread

from bluesky.callbacks.zmq import Publisher
from databroker.core import BlueskyRun
from pkg_resources import resource_filename

import pdfstream.servers.xpd_server as mod

fn = resource_filename("tests", "configs/xpd.ini")


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
    assert len(tmpdir.listdir()) > 0
    for folder in tmpdir.listdir():
        assert len(folder.listdir()) > 0


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
