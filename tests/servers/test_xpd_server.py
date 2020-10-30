import os
import signal
import time
from multiprocessing import Process
from pathlib import Path
from threading import Thread

import databroker
import matplotlib.pyplot as plt
from bluesky.callbacks.zmq import Publisher
from databroker.core import BlueskyRun
from pkg_resources import resource_filename

import pdfstream.servers.xpd_server as mod

fn = resource_filename("tests", "configs/xpd.ini")
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
