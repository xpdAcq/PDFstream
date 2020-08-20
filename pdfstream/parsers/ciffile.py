import json
import typing as tp
from pathlib import Path

from gemmi import cif


def cif_to_dict(cif_file: str, mmjson: bool = False) -> tp.Generator:
    """Convert cif file to a dictionary."""
    cif_path = Path(cif_file)
    doc = cif.read_file(str(cif_path))
    dct: dict = json.loads(
        doc.as_json(mmjson=mmjson)
    )
    if not mmjson:
        for block_name, block_dct in dct.items():
            block_dct['name'] = block_name
            block_dct['cif_file'] = str(cif_path.absolute())
            yield block_dct
    else:
        yield dct
