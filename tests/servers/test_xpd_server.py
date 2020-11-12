from multiprocessing import Process

import databroker
import databroker.v2
import matplotlib.pyplot as plt
import os
import signal
import time
from bluesky.callbacks.zmq import Publisher
from databroker.core import BlueskyRun
from pathlib import Path
from pkg_resources import resource_filename
from tests.callbacks.test_core import fn
from threading import Thread

import pdfstream.servers
import pdfstream.servers.xpd_server as mod

fn = resource_filename("tests", "configs/xpd_server.ini")
plt.ioff()


def interrupt(delay: float) -> None:
    """Keyboard interrupt after delay. Used in testing servers."""
    time.sleep(delay)
    print("Keyboard interrupt ...")
    os.kill(os.getpid(), signal.SIGINT)


def experiment(run: BlueskyRun, delay: float, address: str, prefix: bytes):
    """Send docs to proxy. Used in testing servers."""
    time.sleep(delay)
    publisher = Publisher(address, prefix=prefix)
    for name, doc in run.canonical(fill="yes"):
        publisher(name, doc)
    return


def test_XPDServerConfig():
    config = mod.load_config(fn)
    assert len(config.sections()) > 0


def test_make_and_run_with_proxy(db_with_dark_and_light, proxy, tmpdir):
    raw_db = db_with_dark_and_light
    an_db = databroker.v2.temp()
    process = Process(target=experiment, args=(raw_db[-1], 4, proxy[0], b'raw'), daemon=True)
    thread = Thread(target=interrupt, args=(14,))
    thread.start()
    process.start()
    mod.make_and_run(fn, test_file_base=str(tmpdir), test_an_db=an_db, test_raw_db=raw_db)
    thread.join()
    process.join()
    folder = Path(str(tmpdir))
    assert len(list(folder.rglob("*.tiff"))) > 0
    assert len(list(folder.rglob("*.csv"))) > 0
    assert len(list(folder.rglob("*.json"))) > 0
    assert len(list(an_db)) > 0


def test_XPDRouter(db_with_dark_and_scan, tmpdir):
    raw_db = db_with_dark_and_scan
    an_db = databroker.v2.temp()
    config = pdfstream.servers.xpd_server.XPDConfig()
    config.read(fn)
    config.tiff_base = str(tmpdir)
    config.calib_base = str(tmpdir)
    cb = pdfstream.servers.xpd_server.XPDRouter(config, raw_db=raw_db, an_db=an_db)
    for name, doc in raw_db[-1].canonical(fill="yes", strict_order=True):
        cb(name, doc)
    tiff_base = Path(config.tiff_base)
    assert len(list(tiff_base.rglob("*.tiff"))) > 0
    assert len(list(tiff_base.rglob("*.csv"))) > 0
    assert len(list(tiff_base.rglob("*.json"))) > 0
    assert len(list(an_db)) > 0
