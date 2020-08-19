from gemmi import cif
import json
from pathlib import Path


def cif_to_dict(cif_file: str) -> dict:
    """Convert cif file to a dictionary."""
    cif_path = Path(cif_file)
    doc = cif.read_file(str(cif_path))
    dct = json.loads(
        doc.as_json(mmjson=True)
    )
    dct['file_path'] = str(cif_path.absolute())
    return dct
