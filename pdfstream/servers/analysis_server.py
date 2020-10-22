import rapidz as rz
import typing as tp
from bluesky.callbacks.zmq import Publisher
from bluesky.callbacks.zmq import RemoteDispatcher
from configparser import ConfigParser
from event_model import RunRouter
from pkg_resources import resource_filename

import pdfstream.pipeline.callbacks as callbacks
import pdfstream.pipeline.streams as streams
from pdfstream.pipeline.runrouters import not_dark_numpy_reg_router


class AnalysisServerConfig(ConfigParser):
    @property
    def calibration_md_key(self):
        return self.get("METADATA", "calibration_md_key")

    @property
    def mask_setting(self):
        section = self["MASK SETTING"]
        return {
            "alpha": section.getfloat("alpha"),
            "edge": section.getint("edge"),
            "lower_thresh": section.getfloat("lower_thresh"),
            "upper_thresh": section.getfloat("upper_thresh")
        }

    @property
    def integ_setting(self):
        section = self["INTEGRATION SETTING"]
        return {
            "npt": section.getint("npt"),
            "correctSolidAngle": section.getboolean("correctSolidAngle"),
            "polarization_factor": section.getfloat("polarization_factor"),
            "method": section.get("method"),
            "normalization_factor": section.getfloat("normalization_factor")
        }

    @property
    def pyfai_unit(self):
        return self.get("INTEGRATION SETTING", "unit")

    @property
    def composition_key(self):
        return self.get("METADATA", "composition_key")

    @property
    def wavelength_key(self):
        return self.get("METADATA", "wavelength_key")

    @property
    def trans_setting(self):
        section = self["TRANSFORMATION SETTING"]
        return {
            "rpoly": section.getfloat("rpoly"),
            "qmaxinst": section.getfloat("qmaxinst"),
            "qmin": section.getfloat("qmin"),
            "qmax": section.getfloat("qmax")
        }

    @property
    def grid_config(self):
        section = self["PDF SETTING"]
        return {
            "rmin": section.getfloat("rmin"),
            "rmax": section.getfloat("rmax"),
            "rstep": section.getfloat("rstep")
        }

    @property
    def in_address(self):
        return self.get("PROXY", "in_address")

    @property
    def out_address(self):
        return self.get("PROXY", "out_address")

    @property
    def in_prefix(self):
        return self.get("PROXY", "in_prefix").encode()

    @property
    def out_prefix(self):
        return self.get("PROXY", "out_prefix").encode()


def make_pipeline(
    config: AnalysisServerConfig,
    publishers: tp.List[tp.Callable] = None
) -> rz.Stream:
    """The streaming pipeline of analysis. The data will be published by publisher. If None, create one.
    Return the input node.
    """
    source = rz.Stream(stream_name="document")
    pipeline = [
        callbacks.DarkSubtraction(),
        callbacks.AutoMasking(
            calibration_md_key=config.calibration_md_key,
            mask_setting=config.mask_setting
        ),
        callbacks.AzimuthalIntegration(
            calibration_md_key=config.calibration_md_key,
            integ_setting=config.integ_setting,
            pyfai_unit=config.pyfai_unit
        ),
        callbacks.TransformIQtoFQ(
            composition_key=config.composition_key,
            wavelength_key=config.wavelength_key,
            pyfai_unit=config.pyfai_unit,
            trans_setting=config.trans_setting
        ),
        callbacks.TransformFQtoGr(
            grid_config=config.grid_config
        )
    ]
    nodes = streams.linked_list(source, pipeline)
    if publishers is None:
        publishers = [Publisher(config.out_address, prefix=config.out_prefix) for _ in range(len(nodes))]
    for node, publisher in zip(nodes, publishers):
        rz.starsink(node, publisher)
    return source


def make_router(config: AnalysisServerConfig, publishers: tp.List[tp.Callable] = None) -> RunRouter:
    """Make the analysis router based on the pipeline."""
    source = make_pipeline(config, publishers=publishers)
    cb = callbacks.AnalysisCallback(source)
    return not_dark_numpy_reg_router([cb])


def make_dispatcher(cfg_file: str = None, publishers: tp.List[tp.Callable] = None) -> RemoteDispatcher:
    """Make the remote dispatcher."""
    if cfg_file is None:
        cfg_file = DEFAULT_CFG_FILE
    config = AnalysisServerConfig()
    config.read(cfg_file)
    router = make_router(config, publishers=publishers)
    dispatcher = RemoteDispatcher(config.in_address, prefix=config.in_prefix)
    dispatcher.subscribe(router)
    return dispatcher


DEFAULT_CFG_FILE = resource_filename("pdfstream", "data/analysis_server.ini")


def make_and_run(cfg_file: str = None):
    """Make an analysis server and run it."""
    dispatcher = make_dispatcher(cfg_file)
    print("Start analysis server ...")
    dispatcher.start()
