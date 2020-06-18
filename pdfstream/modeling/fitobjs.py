"""Objects used in the fitting."""
from typing import Union, List, Callable, Dict, Tuple

from diffpy.srfit.fitbase import FitRecipe, ProfileGenerator
from diffpy.structure import Structure
from pyobjcryst.crystal import Crystal
from pyobjcryst.molecule import Molecule

__all__ = ["GenConfig", "FunConfig", "ConConfig", "MyRecipe"]

Stru = Union[Crystal, Molecule, Structure]


class GenConfig:
    """
    A configuration class to provide information in the building of PDFGenerator or DebyePDFGenerator. It is used
    by 'make_generator' in 'myscripts.fittingfunction'.

    Attributes
    ----------
    name : str
        The name of the generator.

    structure : Stru
        The structure object. Options are Crystal, Molecule, Structure.

    periodic : bool
        If the structure if periodic. Default if cif or stru, True else False.

    debye : bool
        Use DebyePDFGenerator or PDFGenerator. Default if periodic, False else True.

    ncpu : int
        number of parallel computing cores for the generator. If None, no parallel. Default None.
    """

    def __init__(self, name: str, structure: Stru, periodic: bool = None, debye: bool = None, ncpu: int = None):
        """Initiate the GenConfig."""
        self.name = name
        self.structure = structure
        self.stru_type = self.get_type(structure)
        self.periodic = self.is_periodic(structure) if periodic is None else periodic
        self.debye = not self.periodic if debye is None else debye
        self.ncpu = ncpu

    @staticmethod
    def is_periodic(structure: Stru) -> bool:
        """If Crystal, Structure, return True. If Molecule, return False"""
        if isinstance(structure, Molecule):
            return False
        return True

    @staticmethod
    def get_type(structure: Stru) -> str:
        """Get the type of the structure obj."""
        type_dct = {
            Crystal: 'crystal',
            Molecule: 'molecule',
            Structure: 'diffpy'
        }
        type_str = type_dct.get(type(structure))
        if type_str is None:
            raise TypeError("Unknown structure type: {}".format(type(structure)))
        return type_str

    def to_dict(self) -> dict:
        """
        Parse the GenConfig as a dictionary. The keys include: gen_name, stru_file, debye, periodic, ncpu.

        Returns
        -------
        config_dct
            A dictionary of generator configuration.

        """
        config_dct = {
            'gen_name': self.name,
            'stru_type': self.stru_type,
            'debye': self.debye,
            'periodic': self.periodic,
            'ncpu': self.ncpu,
        }
        return config_dct


class FunConfig:
    """
    Configuration for the characteristic function.

    Attributes
    ----------
        name
            name of the function, also the name in Fitcontribution.
        func_type
            characteristic function from diffpy cmi.
        argnames
            argument names in the function. it will rename all arguments to avoid conflicts. If None, no renaming.
            If not None, it always starts with "r" when using diffpy characteristic functions. Default None.
    """

    def __init__(self, name: str, func_type: Callable, argnames: List[str] = None):
        """Initiate Function object."""
        self.name = name
        self.func_type = func_type
        self.argnames = argnames


class ConConfig:
    """
    Configuration for the FitContribution.

    Attributes
    ----------
    name : str
        The name of Fitcontribution.

    data_id : int
        The id of the data. It will be used as a foreign key when the results are saved.

    data_file : str
        The path to the data file.

    fit_range
        A tuple of (rmin, rmax, rstep) in angstrom for fitting.

    qparams
        A tuple of (qdamp, qbroad) from calibration.

    eq
        An equation string for the Fitcontribution. If None, use summation of the partial equation.

    partial_eqs
        The mapping from the phase name to the equation of the PDF. If None, partial PDF will not be calculated.

    genconfigs
        A single or a list of GenConfig object. Default empty tuple.

    funconfigs
        A single or a list of FunConfig object. Default empty tuple.

    baselines
        A single or a list of Generator instance of base line. Default empty tuple.

    res_eq
        A string residual equation. Default "chiv".

    weight
        The weight of the contribution. Default 1.
    """

    def __init__(self,
                 name: str,
                 data_id: int,
                 data_file: str,
                 fit_range: Tuple[float, float, float],
                 qparams: Tuple[float, float],
                 partial_eqs: Dict[str, str] = None,
                 eq: str = None,
                 genconfigs: Union[GenConfig, List[GenConfig]] = (),
                 funconfigs: Union[FunConfig, List[FunConfig]] = (),
                 baselines: Union[Callable, List[Callable]] = (),
                 res_eq: str = "res",
                 weight: float = 1.):
        """Initiate the instance."""
        self.name: str = name
        self.data_id: int = data_id
        self.data_file: str = data_file
        self.fit_range: Tuple[float, float, float] = fit_range
        self.qparams: Tuple[float, float] = qparams
        if partial_eqs is None and eq is None:
            raise ValueError("Both partial_eqs and eq are None.")
        elif partial_eqs is None:
            self.eq: str = eq
            self.partial_eqs = None
        elif eq is None:
            self.eq: str = " + ".join(partial_eqs.values())
            self.partial_eqs = partial_eqs
        else:
            self.eq = eq
            self.partial_eqs = partial_eqs
        self.genconfigs: List[GenConfig] = _make_list(genconfigs)
        self.funconfigs: List[FunConfig] = _make_list(funconfigs)
        self.baselines: List[ProfileGenerator] = _make_list(baselines)
        self.res_eq: str = res_eq
        self.weight = weight

    def to_dict(self) -> dict:
        """
        Parse the ConConfig to a dictionary. The keys will include: con_name, data_id, data_file, rmin, rmax, dr, qdamp,
        qbroad, eq, phases, functions, base_lines, res_eq.

        Returns
        -------
        config_dct
            A dictionary of configuration of FitContribution.
        """
        config_dct = {
            'con_name': self.name,
            'data_id': self.data_id,
            'data_file': self.data_file,
            'rmin': self.fit_range[0],
            'rmax': self.fit_range[1],
            'dr': self.fit_range[2],
            'qdamp': self.qparams[0],
            'qbroad': self.qparams[1],
            'eq': self.eq,
            'phases': ', '.join([gen.name for gen in self.funconfigs]),
            'functions': ', '.join([fun.name for fun in self.funconfigs]),
            'baselines': ', '.join([bl.name for bl in self.baselines]),
            'res_eq': self.res_eq
        }
        return config_dct


class MyRecipe(FitRecipe):
    """
    The FitRecipe with augmented features.

    Attributes
    ----------
    configs
        single or multiple configurations to initiate the contributions in recipe.
    """

    def __init__(self, configs: Tuple[ConConfig]):
        """Initiate the class."""
        super().__init__()
        self.configs = configs


def _make_list(item) -> list:
    """If item is not a list or tuple, make it a list with only the item in it."""
    if isinstance(item, (list, tuple)):
        pass
    else:
        item = [item]
    return item
