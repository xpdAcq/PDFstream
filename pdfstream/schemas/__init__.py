import json
from pathlib import Path

from event_model import DocumentNames, _Validator
from pkg_resources import resource_filename as rs_fn

__all__ = [
    "analysis_in_schemas",
    "analysis_out_schemas",
    "Validator",
    "DocumentNames"
]

ANALYSIS_IN_SCHEMA_NAMES = {
    DocumentNames.start: 'schemas/analysis_in/run_start.json',
    DocumentNames.stop: 'schemas/analysis_in/run_stop.json',
    DocumentNames.event: 'schemas/analysis_in/event.json',
    DocumentNames.event_page: 'schemas/analysis_in/event_page.json',
    DocumentNames.descriptor: 'schemas/analysis_in/event_descriptor.json',
    DocumentNames.datum: 'schemas/analysis_in/datum.json',
    DocumentNames.datum_page: 'schemas/analysis_in/datum_page.json',
    DocumentNames.resource: 'schemas/analysis_in/resource.json'
}

analysis_in_schemas = {}
for doc_name, filename in ANALYSIS_IN_SCHEMA_NAMES.items():
    with Path(rs_fn('pdfstream', filename)).open("r") as fin:
        analysis_in_schemas[doc_name] = json.load(fin)

ANALYSIS_OUT_SCHEMA_NAMES = {
    DocumentNames.start: 'schemas/analysis_out/run_start.json',
    DocumentNames.stop: 'schemas/analysis_out/run_stop.json',
    DocumentNames.event: 'schemas/analysis_out/event.json',
    DocumentNames.event_page: 'schemas/analysis_out/event_page.json',
    DocumentNames.descriptor: 'schemas/analysis_out/event_descriptor.json',
    DocumentNames.datum: 'schemas/analysis_out/datum.json',
    DocumentNames.datum_page: 'schemas/analysis_out/datum_page.json',
    DocumentNames.resource: 'schemas/analysis_out/resource.json'
}

analysis_out_schemas = {}
for doc_name, filename in ANALYSIS_OUT_SCHEMA_NAMES.items():
    with Path(rs_fn('pdfstream', filename)).open("r") as fin:
        analysis_out_schemas[doc_name] = json.load(fin)


def print_data_keys(schemas: dict):
    """Print out data keys in event descriptor."""
    data_keys: dict = schemas[DocumentNames.descriptor]['properties']['data_keys']
    for k, v in data_keys.get("properties", {}).items():
        print("{}: {}".format(k, v.get("description", "")))


class Validator(object):
    """The json schema validator wrapped in a bluesky callback.

    Attributes
    ----------
    schemas : dict
        A mapping from the doc name to the schemas for that doc.
    """
    document_names = {
        "start": DocumentNames.start,
        "stop": DocumentNames.stop,
        "event": DocumentNames.event,
        "event_page": DocumentNames.event_page,
        "descriptor": DocumentNames.descriptor,
        "datum": DocumentNames.datum,
        "datum_page": DocumentNames.datum_page,
        "resource": DocumentNames.resource
    }

    def __init__(self, schemas: dict):
        self.schemas = schemas

    def __call__(self, name: str, doc: dict):
        doc_type = self.document_names[name]
        schema = self.schemas[doc_type]
        validator = _Validator(schema=schema)
        validator.validate(doc)
