from multiprocessing import Process

import os
import signal
import time
from bluesky.callbacks.zmq import Publisher
from databroker.core import BlueskyRun
from databroker.v2 import temp
from pkg_resources import resource_filename
from threading import Thread

import pdfstream.servers.analysis_server as an

fn = resource_filename("pdfstream", "data/analysis_server.ini")
fn1 = resource_filename("pdfstream", "data/viz_server.ini")


def test_AnalysisServerConfig():
    config = an.AnalysisServerConfig()
    config.read(fn)
    assert config.calibration_md_key == "calibration_md"
    assert config.composition_key == "sample_composition"
    assert config.wavelength_key == "bt_wavelength"
    assert config.mask_setting == {
        "alpha": 2.0,
        "edge": 20,
        "lower_thresh": 0.,
        "upper_thresh": None
    }
    assert config.integ_setting == dict(
        npt=1024,
        correctSolidAngle=False,
        polarization_factor=0.99,
        method="splitpixel",
        normalization_factor=1.0,
    )
    assert config.pyfai_unit == "q_A^-1"
    assert config.trans_setting == dict(
        rpoly=1.0,
        qmaxinst=24.0,
        qmin=0.0,
        qmax=22.0
    )
    assert config.grid_config == dict(
        rmin=0.0,
        rmax=30.0,
        rstep=0.01
    )
    assert config.in_prefix == b'raw'
    assert config.in_address == "127.0.0.1:5568"
    assert config.out_address == "127.0.0.1:5567"
    assert config.out_prefix == b'an'


def test_make_router(run0):
    # analysis
    config = an.AnalysisServerConfig()
    config.read(fn)
    db = temp()
    router = an.make_router(config, db=db)
    for name, doc in run0.canonical(fill="yes"):
        router(name, doc)
    print(db[-1].metadata['start'])
    print(db[-1].primary.read())


def test_make_dispatcher(proxy):
    an.make_dispatcher()


def interrupt(delay: float) -> None:
    time.sleep(delay)
    print("Keyboard interrupt ...")
    os.kill(os.getpid(), signal.SIGINT)


def experiment(run: BlueskyRun, delay: float, address: str):
    time.sleep(delay)
    publisher = Publisher(address, prefix=b'raw')
    for name, doc in run.canonical(fill="yes"):
        publisher(name, doc)
    return


def test_make_and_run(run0, proxy):
    process = Process(target=experiment, args=(run0, 1, proxy[0]), daemon=True)
    thread = Thread(target=interrupt, args=(7,))
    thread.start()
    process.start()
    an.make_and_run(fn)
    thread.join()
    process.join()
