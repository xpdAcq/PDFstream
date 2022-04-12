"""Event model run composer from files."""
import time
import typing as tp
import uuid

import numpy as np
from event_model import compose_run, ComposeDescriptorBundle


def gen_stream(
    data_lst: tp.List[dict],
    metadata: dict,
    uid: str = None
) -> tp.Generator[tp.Tuple[str, dict], None, None]:
    """Generate a fake doc stream from data and metadata."""
    crb = compose_run(metadata=metadata, uid=uid if uid else str(uuid.uuid4()))
    yield "start", crb.start_doc
    if len(data_lst) == 0:
        yield "stop", crb.compose_stop()
    else:
        cdb: ComposeDescriptorBundle = crb.compose_descriptor(
            name="primary",
            data_keys=compose_data_keys(data_lst[0])
        )
        yield "descriptor", cdb.descriptor_doc
        for data in data_lst:
            yield "event", cdb.compose_event(data=data, timestamps=compose_timestamps(data))
        yield "stop", crb.compose_stop()


def compose_data_keys(data: tp.Dict[str, tp.Any]) -> tp.Dict[str, dict]:
    """Compose the data keys."""
    return {k: dict(**compose_data_info(v), source="PV:{}".format(k.upper())) for k, v in data.items()}


def compose_data_info(value: tp.Any) -> dict:
    """Compose the data information."""
    if isinstance(value, str):
        return {"dtype": "string", "shape": []}
    elif isinstance(value, float):
        return {"dtype": "number", "shape": []}
    elif isinstance(value, bool):
        return {"dtype": "boolean", "shape": []}
    elif isinstance(value, int):
        return {"dtype": "integer", "shape": []}
    else:
        return {"dtype": "array", "shape": np.shape(value)}


def compose_timestamps(data: tp.Dict[str, tp.Any]) -> tp.Dict[str, float]:
    """Compose the fake time for the data measurement."""
    return {k: time.time() for k in data.keys()}
