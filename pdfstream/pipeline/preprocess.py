import event_model
import typing
from databroker.core import BlueskyRun


def unpack_pages(name: str, doc) -> typing.Generator:
    """Unpack the dataum_page and event_page. Return a list of document."""
    if name == "datum_page":
        for d in event_model.unpack_datum_page(doc):
            yield "datum", d
    elif name == "event_page":
        for d in event_model.unpack_event_page(doc):
            yield "event", d
    else:
        yield name, doc


def is_allowed_type(doc_tup: tuple, doc_types: frozenset) -> bool:
    """If the document type in doc_types return True. Else False."""
    if doc_tup[0] in doc_types:
        return True
    return False


def basic_doc_stream(run: BlueskyRun) -> typing.Generator:
    """Unpack the docs from a run and yield the type in start, descriptor, event and stop."""
    for name, doc in run.canonical(fill="yes"):
        for _name, _doc in unpack_pages(name, doc):
            if _name in ["start", "descriptor", "event", "stop"]:
                yield _name, _doc
