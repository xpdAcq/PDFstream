import rapidz as rz
import typing as tp

import pdfstream.pipeline.preprocess as pp


def linked_list(source: rz.Stream, cbs: tp.List[tp.Callable]) -> tp.List[rz.Stream]:
    """Make a stream using a linked list of callback functions. Return the list of nodes."""
    lst = []
    for cb in cbs:
        source = rz.starmap(source, cb)
        lst.append(source)
    return lst


def doc_preprocess(
    source: rz.Stream,
    doc_types: frozenset = frozenset(["start", "descriptor", "event", "event_page", "stop"])
) -> tp.List[rz.Stream]:
    """Filter the type, unpack the page doc and emit one by one. Return unpack, filter and flatten
    nodes.
    """
    node0 = rz.filter(source, pp.is_allowed_type, doc_types=doc_types, stream_name="DocFilter")
    node1 = rz.starmap(node0, pp.unpack_pages, stream_name="DocUnpacker")
    node2 = rz.flatten(node1, stream_name="DocEmitter")
    return [node0, node1, node2]
