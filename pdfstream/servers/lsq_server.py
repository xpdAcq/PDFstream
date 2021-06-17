import typing as tp
from collections import namedtuple
from configparser import ConfigParser
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from area_detector_handlers.handlers import AreaDetectorTiffHandler
from bluesky.callbacks.stream import LiveDispatcher
from diffpy.pdfgetx import PDFGetter, PDFConfig
from event_model import RunRouter
from ophyd.sim import NumpySeqHandler

import pdfstream.units as units
from pdfstream.callbacks.basic import LiveWaterfall, NumpyExporter
from pdfstream.servers.base import ServerConfig, BaseServer


class LSQConfig(ConfigParser):
    """The configuration to make LSQ run router."""

    def __init__(self, *args, **kwargs):
        super(LSQConfig, self).__init__(*args, **kwargs)
        self._figs = list()

    @property
    def data_config(self):
        section = self["DATA KEYS"]
        tup = namedtuple(
            "data_config",
            ["x", "y", "lsq_type", "comp_id", "lsq_comps", "composition"]
        )
        return tup(
            section.get("x"),
            section.get("y"),
            section.get("lsq_type"),
            section.get("comp_id"),
            section.get("lsq_comps"),
            section.get("composition")
        )

    @property
    def interp_config(self):
        section = self["INTERPOLATION"]
        tup = namedtuple("interp_config", ["x"])
        tup.x = np.arange(
            section.getfloat("xmin"),
            section.getfloat("xmax"),
            section.getfloat("xstep")
        )
        return tup

    @property
    def fit_config(self):
        section = self["FITTING"]
        tup = namedtuple("fit_config", ["p"])
        tup.p = section.getfloat("p")
        return tup

    @property
    def trans_config(self):
        section = self["TRANSFORMATION"]
        return dict(
            dataformat=section.get("dataformat"),
            qmin=section.getfloat("qmin"),
            qmax=section.getfloat("qmax"),
            qmaxinst=section.getfloat("qmaxinst"),
            rpoly=section.getfloat("rpoly"),
            rmin=section.getfloat("rmin"),
            rmax=section.getfloat("rmax"),
            rstep=section.getfloat("rstep")
        )

    @property
    def export_config(self):
        section = self["EXPORTATION"]
        tup = namedtuple("export_config", ["directory", "file_prefix"])
        tup.directory = Path(section.get("directory"))
        tup.file_prefix = section.get("file_prefix")
        return tup

    @property
    def verbose(self):
        return self.getint("BASIC", "verbose", fallback=1)


class LSQServerConfig(LSQConfig, ServerConfig):
    """The configuration to make LSQ server."""
    pass


class LSQServer(BaseServer):
    """The server that decomposes one array data to a linear combination of the several array data in the record
    and save the data and visualize the residual of the decomposition and the PDF data transformed from it."""

    def __init__(self, config: LSQServerConfig):
        super(LSQServer, self).__init__(config)
        self.subscribe(LSQRunRouter(config))

    @classmethod
    def from_config(cls, config: LSQServerConfig):
        return LSQServer(config)

    @classmethod
    def from_cfg_file(cls, cfg_file: str):
        config = LSQServerConfig()
        config.read(cfg_file)
        return LSQServer(config)


class LSQRunRouter(RunRouter):
    """The run router that send the documents that can be processed by the decomposer."""

    def __init__(self, config: LSQConfig):
        factory = LSQFactory(config)
        super(LSQRunRouter, self).__init__(
            [factory],
            handler_registry={
                "NPY_SEQ": NumpySeqHandler,
                "AD_TIFF": AreaDetectorTiffHandler
            }
        )


class LSQFactory:
    """The factory to generate the callbacks for the lsq run router."""

    def __init__(self, config: LSQConfig):
        self.config = config
        self.decomposer = LiveDecomposer(config)
        self.decomposer.subscribe(Visualiser(config))
        self.decomposer.subscribe(Exporter(config))

    def __call__(self, name, doc):
        if name == "start" and doc.get(self.config.data_config.lsq_type) is not None:
            return [self.decomposer], []
        return [], []


class LiveDecomposer(LiveDispatcher):
    """A callback to decompose one array data to a linear combination of the several array data in the record
    and transform the data to PDF."""

    def __init__(self, config: LSQConfig):
        super(LiveDecomposer, self).__init__()
        self.config = config
        self.memory = dict()
        self.cache = dict()

    def start(self, doc, _md=None):
        self.cache = dict()
        keys = self.config.data_config
        # get the type of the data, target, components or neither
        self.cache["lsq_type"] = doc.get(keys.lsq_type)
        # if it is target, there is a list of keys in memory, pointing to the data for decomposition
        self.cache["lsq_comps"] = doc.get(keys.lsq_comps, [])
        # if it is component, use the sample as the key in memory
        self.cache["comp_id"] = doc.get(keys.comp_id, "")
        # sample composition for pdfconfig
        self.cache["composition"] = doc.get(keys.composition, "C")
        super(LiveDecomposer, self).start(doc, _md=_md)

    def event(self, doc, _md=None):
        # if target, process the data and emit descriptor and events
        if self.cache["lsq_type"] == "target":
            if self.config.verbose > 0:
                print("Process data from the {}.".format(self.cache["comp_id"]))
            data = process_data(
                data=doc["data"],
                memory=self.memory,
                lsq_comps=self.cache["lsq_comps"],
                composition=self.cache["composition"],
                config=self.config
            )
            self.process_event({"data": data, 'descriptor': doc["descriptor"]})
        # if components, record the interpreted data in memory
        elif self.cache["lsq_type"] == "component":
            if self.config.verbose > 0:
                print("Record data from the {} in memory.".format(self.cache["comp_id"]))
            self.memory[self.cache["comp_id"]] = get_interp_data(doc["data"], self.config)
        # else do nothing
        else:
            pass

    def stop(self, doc, _md=None):
        self.cache = dict()
        super(LiveDecomposer, self).stop(doc, _md=_md)


def process_data(
    data: tp.Dict[str, np.ndarray],
    memory: tp.Dict[str, np.ndarray],
    lsq_comps: tp.List[str],
    composition: str,
    config: LSQConfig
) -> tp.Dict[str, np.ndarray]:
    """Process the data from the event."""
    # the interpolated target y data
    y = get_interp_data(data, config)
    # the component matrix where each row is a component data
    x = np.stack([memory[k] for k in lsq_comps], axis=0)
    # the model to decompose to a weight and the component matrix.
    model = Model(y, x, config.fit_config.p, xgrid=config.interp_config.x)
    opt.least_squares(model.cost_func, x0=model.x0)
    # transfer the data to PDF
    pdfconfig = PDFConfig(**config.trans_config, composition=composition)
    pdfgetter = PDFGetter(pdfconfig)
    pdfgetter(model.xgrid, model.yres)
    return {
        "y": model.y,
        "x": model.x,
        "w": model.w,
        "xgrid": model.xgrid,
        "yres": model.yres,
        "r": pdfgetter.gr[0],
        "g": pdfgetter.gr[1]
    }


def get_interp_data(data: tp.Dict[str, np.ndarray], config: LSQConfig) -> np.ndarray:
    """Get the x and y data from the data in event."""
    xp = data[config.data_config.x]
    yp = data[config.data_config.y]
    x = config.interp_config.x
    y = np.interp(x, xp, yp)
    return y


class Model:
    """The calculate Y - P(wX^T). Y is the a vector, P is a mapping from vector to vector, Pv = v'. v'_i =
    sqrt(p) v_i if v_i > 0 else v'_i = sqrt(1 - p) v_i. w is the vector and X is a matrix."""

    def __init__(self, y: np.ndarray, x: np.ndarray, p: float, xgrid=None):
        self.y = y
        self.x = x
        self.ycalc = None
        self.w = None
        self.yres = None
        self.xgrid = xgrid
        self.pos = np.sqrt(p)
        self.neg = np.sqrt(1 - p)

    def cost_func(self, w: np.ndarray):
        self.w = w
        self.ycalc = np.dot(w, self.x)
        self.yres = self.y - self.ycalc
        return np.where(self.yres > 0, self.pos * self.yres, self.neg * self.yres)

    @property
    def x0(self):
        return np.zeros(self.x.shape[0])


class Visualiser(RunRouter):
    """The callback to visualize documents from the decomposer."""

    def __init__(self, config: LSQConfig):
        factory = VisualiserFactory(config)
        super(Visualiser, self).__init__([factory], handler_registry={"NPY_SEQ": NumpySeqHandler})


class VisualiserFactory:
    """The factory of the visualizer."""

    def __init__(self, config: LSQConfig):
        self.config = config
        fig = plt.figure()
        self.callbacks = [
            LiveWaterfall(
                "xgrid",
                "yres",
                xlabel=units.LABELS.iq[0],
                ylabel=units.LABELS.iq[1],
                ax=fig.add_subplot(121)
            ),
            LiveWaterfall(
                "r",
                "g",
                xlabel=units.LABELS.gr[0],
                ylabel=units.LABELS.gr[1],
                ax=fig.add_subplot(122)
            )
        ]
        fig.show()

    def __call__(self, name, doc):
        if name == "start" and doc.get(self.config.data_config.lsq_type) == "target":
            return self.callbacks, []
        return [], []


class Exporter(RunRouter):
    """The callback to export documents from the decomposer."""

    def __init__(self, config: LSQConfig):
        factory = ExporterFactory(config)
        super(Exporter, self).__init__([factory], handler_registry={"NPY_SEQ": NumpySeqHandler})


class ExporterFactory:
    """The factory of the exporter."""

    def __init__(self, config: LSQConfig):
        self.config = config
        self.callbacks = [
            NumpyExporter(
                str(config.export_config.directory),
                file_prefix=config.export_config.file_prefix,
                data_keys=["y", "x", "w", "xgrid", "yres", "r", "g"]
            )
        ]

    def __call__(self, name, doc):
        if name == "start" and doc.get(self.config.data_config.lsq_type) == "target":
            return self.callbacks, []
        return [], []


def make_and_run(cfg_file: str = None, test_mode: bool = False):
    """Make and run LSQ server."""
    server = LSQServer.from_cfg_file(cfg_file)
    if not test_mode:
        server.install_qt_kicker()
        server.start()
