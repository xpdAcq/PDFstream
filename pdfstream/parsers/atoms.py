from ase import Atoms, Atom
from ase.spacegroup import crystal

import pdfstream.parsers.tools as tools


def dict_to_atoms(dct: dict, keys: tuple, **kwargs) -> Atoms:
    """Parse the structure information inside a document into an ase.Atoms object."""
    return stru_dict_to_crystal(
        tools.get_value(dct, keys),
        **kwargs
    )


def stru_dict_to_crystal(dct: dict, **kwargs) -> Atoms:
    """Parse a dictionary of structure information to an ase.Atoms object."""
    return crystal(
        symbols=list(map(atom_dict_to_atom, dct['atoms'])),
        cellpar=lat_dict_to_list(dct["lattice"]),
        spacegroup=dct["space_group"],
        occupancies=get_occ_list(dct["atoms"]),
        **kwargs
    )


def atom_dict_to_atom(dct: dict) -> Atom:
    """Parse a dictionary of atom information to an ase.Atom object."""
    return Atom(
        symbol=tools.only_letter(dct["element"]),
        tag=int(tools.only_digit(dct["name"])),
        position=(dct["x"], dct["y"], dct["z"]),
    )


def lat_dict_to_list(dct: dict) -> list:
    """Make a dictionary of lattice information to a 6-vector [a, b, c, alpha, beta, gamma]."""
    return [
        dct[k] for k in ("a", "b", "c", "alpha", "beta", "gamma")
    ]


def get_occ_list(lst: list) -> list:
    """Get the occupancies list from a list of atom information dictionary."""
    return [
        doc["occ"] for doc in lst
    ]
