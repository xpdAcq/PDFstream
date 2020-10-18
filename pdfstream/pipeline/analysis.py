"""A streaming pipeline factory."""
import rapidz
import typing
from databroker import catalog
from databroker.v2 import Broker
from event_model import RunRouter
from ophyd.sim import NumpySeqHandler
from rapidz import Stream
from shed import AlignEventStreams, ToEventStream, FromEventStream

import pdfstream.pipeline.callbacks as callbacks
import pdfstream.pipeline.from_event as from_event
import pdfstream.pipeline.from_start as from_start
import pdfstream.pipeline.preprocess as preprocess
import pdfstream.pipeline.process as process


def analysis_router(sources: typing.List[Stream]) -> RunRouter:
    router = RunRouter(
        [
            lambda name, doc: (
                [lambda *x: source.emit(x) for source in sources],
                []
            )
            if name == "start" and not doc.get("dark_frame")
            else ([], [])
        ],
        handler_registry={"NPY_SEQ": NumpySeqHandler}
    )
    return router


def streaming_process_img_to_pdf(
    stream_config: typing.Dict[str, typing.Any],
    test_db: Broker = None
) -> typing.Dict[str, Stream]:
    nodes = dict()
    db = catalog[stream_config["db"]] if test_db is None else test_db

    source = Stream(stream_name="source")
    nodes[source.name] = source
    doc_lst = rapidz.map(
        source,
        preprocess.unpack_pages,
        stream_name="doc list"
    )
    nodes[doc_lst.name] = doc_lst
    doc = rapidz.flatten(
        doc_lst,
        stream_name="doc"
    )
    nodes[doc] = doc.name
    start = FromEventStream(
        "start",
        tuple(),
        upstream=doc,
        stream_name="start",
        principle=True
    )
    nodes[start.name] = start
    ai = rapidz.map(
        start,
        from_start.query_ai,
        calibration_md_key=stream_config["calibration_md_key"],
        stream_name="geometry"
    )
    nodes[ai.name] = ai
    dk_img = rapidz.map(
        start,
        from_start.query_dk_img,
        det_name=stream_config["det_name"],
        db=db,
        dk_id_key=stream_config["dk_id_key"],
        stream_name="dark image"
    )
    nodes[dk_img.name] = dk_img
    nodes["dark subtracted background"] = bg_img = rapidz.map(
        start,
        from_start.query_bg_img,
        bg_id_key=stream_config["bg_id_key"],
        det_name=stream_config["det_name"],
        db=db,
        dk_id_key=stream_config["dk_id_key"],
        stream_name="dark subtracted background image"
    )
    config = rapidz.map(
        start,
        from_start.query_bt_info,
        composition_key=stream_config["composition_key"],
        wavelength_key=stream_config["wavelength_key"],
        stream_name="pdfgetx info"
    )
    nodes[config.name] = config
    event = FromEventStream(
        "event",
        tuple(),
        upstream=doc,
        stream_name="event"
    )
    nodes[event.name] = event
    img = rapidz.map(
        event,
        from_event.get_image_from_event,
        det_name=stream_config["det_name"],
        stream_name="raw image"
    )
    nodes[img.name] = img
    raw = rapidz.combine_latest(
        img, ai, dk_img, bg_img, config,
        stream_name="raw data"
    )
    nodes[raw.name] = raw
    result = rapidz.starmap(
        raw,
        process.process_img_to_pdf,
        bg_scale=stream_config["bg_scale"],
        mask_setting=stream_config["mask_setting"],
        integ_setting=stream_config["integ_setting"],
        pdf_setting=stream_config["pdf_setting"],
        stream_name="process data"
    )
    nodes[result.name] = result
    strip_dep_var = callbacks.StripDepVar()
    striped_doc = rapidz.starmap(
        doc,
        strip_dep_var,
        stream_name="strip dependent variables"
    )
    nodes[striped_doc.name] = striped_doc
    for args, kwargs in [
        [
            (0, "raw image"),
            {}
        ],
        [
            (1, "dark subtracted image"),
            {}],
        [
            (2, "background subtracted image"),
            {}
        ],
        [
            (3, "masked image"),
            {}
        ],
        [
            (4, "I(Q)"),
            {
                "hints": {"dimensions": [(["Q"], "primary")]},
                "data_keys": {"Q": {"units": "1/A"}, "I": {"units": "arb"}}
            }
        ],
        [
            (5, "S(Q)"),
            {
                "hints": {"dimensions": [(["Q"], "primary")]},
                "data_keys": {"Q": {"units": "1/A"}, "S": {"units": "arb"}}
            },
        ],
        [
            (6, "F(Q)"),
            {
                "hints": {"dimensions": [(["Q"], "primary")]},
                "data_keys": {"Q": {"units": "1/A"}, "F": {"units": "1/A"}}
            }
        ],
        [
            (7, "G(r)"),
            {
                "hints": {"dimensions": [(["r"], "primary")]},
                "data_keys": {"r": {"units": "A"}, "G": {"units": "1/A**2"}}
            }
        ]
    ]:
        for node in inject_data_to_doc(result, striped_doc, *args, **kwargs):
            nodes[node.name] = node
    return nodes


def inject_data_to_doc(
    data: Stream,
    doc: Stream,
    index: typing.Union[str, int],
    stream_name: str,
    **kwargs
) -> typing.Tuple[Stream, Stream, Stream]:
    node0 = rapidz.pluck(data, index, stream_name=stream_name)
    node1 = ToEventStream(
        node0,
        stream_name="{} doc".format(node0.name),
        **kwargs
    )
    node2 = AlignEventStreams(node1, doc, stream_name="aligned {}".format(node1.name))
    return node0, node1, node2
