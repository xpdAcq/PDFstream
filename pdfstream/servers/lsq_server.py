from collections import namedtuple

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import typing as tp
from bluesky.callbacks.core import CallbackBase
from bluesky.callbacks.stream import LiveDispatcher
from bluesky.callbacks.zmq import RemoteDispatcher
from configparser import ConfigParser
from diffpy.pdfgetx import PDFGetter, PDFConfig
from event_model import RunRouter, unpack_event_page
from ophyd.sim import NumpySeqHandler
from pathlib import Path
from xpdview.waterfall import Waterfall

import pdfstream.units as units
from .config import ServerConfig
from .tools import run_server


class LSQConfig(ConfigParser):
    """The configuration to make LSQ run router."""

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
        return tup.p

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
        return self.getint("OTHER", "verbose")


class LSQServerConfig(LSQConfig, ServerConfig):
    """The configuration to make LSQ server."""
    pass


class LSQServer(RemoteDispatcher):
    """The server that decomposes one array data to a linear combination of the several array data in the record
    and save the data and visualize the residual of the decomposition and the PDF data transformed from it."""

    def __init__(self, config: LSQServerConfig):
        super(LSQServer, self).__init__(config.address, prefix=config.prefix)
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
        super(LSQRunRouter, self).__init__([factory], handler_registry={"NPY_SEQ": NumpySeqHandler})


class LSQFactory:
    """The factory to generate the callbacks for the lsq run router."""

    def __init__(self, config: LSQConfig):
        self.config = config
        self.decomposer = LiveDecomposer(config)
        self.decomposer.subscribe(Visualiser())
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
                doc["data"],
                self.memory,
                self.cache["lsq_comps"],
                self.cache["composition"],
                self.config
            )
            self.process_event({"data": data, 'descriptor': doc["descriptor"]})
        # if components, record the interpreted data in memory
        elif self.cache["lsq_type"] == "component":
            if self.config.verbose > 0:
                print("Record data from the {} in memory.".format(self.cache["comp_id"]))
            self.memory[self.component_id] = get_interp_data(doc["data"], self.config)
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
    x = np.stack([memory[k] for k in lsq_comps])
    # the model to decompose to a weight and the component matrix.
    model = Model(y, x, config.fit_config.p)
    result = opt.least_squares(model.cost_func, x0=model.x0, bounds=config.fit_config.bounds)
    yres = model.cost_func(result.x)
    # transfer the data to PDF
    pdfconfig = PDFConfig(**config.trans_config, composition=composition)
    pdfgetter = PDFGetter(pdfconfig)
    xres = config.fit_config.x
    pdfgetter(xres, yres)
    return {
        "y": y,
        "x": x,
        "w": res.x,
        "xres": config.fit_config.x,
        "yres": yres,
        "r": pdfgetter.gr[0],
        "g": pdfconfig.gr[1]
    }


def get_interp_data(data: tp.Dict[str, np.ndarray], config: LSQConfig) -> np.ndarray:
    """Get the x and y data from the data in event."""
    xp = data[config.data_config.x]
    yp = data[config.data_config.y]
    x = config.fit_config.x
    y = np.interp(x, xp, yp)
    return y


class Model:
    """The calculate Y - P(wX^T). Y is the a vector, P is a mapping from vector to vector, Pv = v'. v'_i =
    \sqrt(p) v_i if v_i > 0 else v'_i = \sqrt(1 - p) v_i. w is the vector and X is a matrix."""

    def __init__(self, y: np.ndarray, x: np.ndarray, p: float):
        self._y = y
        self._x = x
        self._pos = np.sqrt(p)
        self._neg = np.sqrt(1 - p)

    def cost_func(self, w: np.ndarray):
        y = np.inner(w, x)
        yres = self._y - y
        mask = yres > 0.
        return p * yres[mask] + (1. - p) * yres[~mask]

    @property
    def x0(self):
        return np.zeros(self._x.shape[0])


class Visualiser(RunRouter):
    """The callback to visualize documents from the decomposer."""

    def __init__(self):
        factory = VisualiserFactory(config)
        super(Visualiser, self).__init__([factory], handler_registry={"NPY_SEQ": NumpySeqHandler})


class VisualiserFactory:
    """The factory of the visualizer."""

    def __init__(self, config: LSQConfig):
        self.config = config
        self.callbacks = [
            LiveWaterfall("xres", "yres", xlabel=units.LABELS.iq[0], ylabel=units.LABELS.iq[1]),
            LiveWaterfall("r", "g", xlabel=units.LABELS.gr[0], ylabel=units.LABELS.gr[1])
        ]

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
                data_keys=["y", "x", "w", "xres", "yres", "r", "g"]
            )
        ]

    def __call__(self, name, doc):
        if name == "start" and doc.get(self.config.data_config.lsq_type) == "target":
            return self.callbacks, []
        return [], []


class NumpyExporter(CallbackBase):
    """An exporter to export the array data in .npy file."""

    def __init__(self, directory: str, file_prefix: str, data_keys: tp.List[str]):
        super(NumpyExporter, self).__init__()
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.file_template = file_prefix + "{data_key}-{event[seq_num]}.npy"
        self.data_keys = data_keys
        self.cache = dict()

    def start(self, doc):
        self.cache = dict()
        self.cache["start"] = doc
        super(NumpyExporter, self).start(doc)

    def event_page(self, doc):
        for event in unpack_event_page(doc):
            self.event(event)

    def event(self, doc):
        for data_key in self.data_keys:
            arr: np.ndarray = doc["data"][data_key]
            filename = self.file_template.format(start=self.cache["start"], event=doc, data_key=data_key)
            filepath = self.directory.joinpath(filename)
            np.save(str(filepath), arr)
        super(NumpyExporter, self).event(doc)

    def stop(self, doc):
        self.cache = dict()
        super(NumpyExporter, self).stop(doc)


class LiveWaterfall(CallbackBase):
    """A live water plot for the one dimensional data."""

    def __init__(self, x: str, y: str, *, xlabel: str, ylabel: str, **kwargs):
        """Initiate the instance.

        Parameters
        ----------
        x :
            The key of the independent variable.

        y :
            The key of the dependent variable.

        xlabel :
            The tuple of the labels of x shown in the figure.

        ylabel :
            The tuple of the labels of y shown in the figure.

        kwargs :
            The kwargs for the matplotlib.pyplot.plot.
        """
        super().__init__()
        self.x = x
        self.y = y
        fig = plt.figure()
        self.waterfall = Waterfall(fig=fig, unit=(xlabel, ylabel), **kwargs)
        fig.show()

    def start(self, doc):
        super(LiveWaterfall, self).start(doc)
        self.waterfall.clear()

    def event(self, doc):
        super(LiveWaterfall, self).event(doc)
        x_data = doc["data"][self.x]
        y_data = doc["data"][self.y]
        key = doc['seq_num']
        self.update(key, (x_data, y_data))

    def update(self, key: str, int_data: tp.Tuple[np.ndarray, np.ndarray]):
        self.waterfall.update(key_list=[key], int_data_list=[int_data])


def make_and_run(cfg_file: str = "~/.config/acq/lsq_server.ini"):
    """Make and run LSQ server."""
    server = LSQServer.from_cfg_file(cfg_file)
    run_server(server)
    return
