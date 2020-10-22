from pkg_resources import resource_filename

import pdfstream.servers.analysis_server as mod

fn = resource_filename("pdfstream", "data/analysis_server.ini")


def test_AnalysisServerConfig():
    config = mod.AnalysisServerConfig()
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
    assert config.out_prefix == b'an'
    assert config.in_address == '127.0.0.1:5568'
    assert config.out_address == '127.0.0.1:5567'


def test_make_router(run0):
    config = mod.AnalysisServerConfig()
    config.read(fn)
    pubs = [lambda *x: print(x[0], x[1]['uid'])] * 5
    router = mod.make_router(config, pubs)
    for name, doc in run0.canonical(fill="yes"):
        router(name, doc)


def test_make_dispatcher(proxy):
    mod.make_dispatcher()
