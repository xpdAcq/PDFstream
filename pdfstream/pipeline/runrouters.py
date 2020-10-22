import typing as tp
from event_model import RunRouter
from ophyd.sim import NumpySeqHandler


def not_dark_numpy_reg_router(callbacks: tp.List[tp.Callable]) -> RunRouter:
    """Make a RunRouter that only reacts to the data not from dark frame run and registered with a numpy
    handler. It will be used to build analysis server."""

    def factory(name, doc):
        if name == "start" and not doc.get("dark_frame"):
            return callbacks, []
        return [], []

    return RunRouter(factories=[factory], handler_registry={"NPY_SEQ": NumpySeqHandler})
