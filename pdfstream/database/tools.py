import math
import typing as tp

from diffpy.srfit.fitbase import FitRecipe
from diffpy.srfit.fitbase.fitresults import FitResults, ContributionResults
from diffpy.srfit.pdf import PDFGenerator, DebyePDFGenerator
from diffpy.srfit.structure.srrealparset import SrRealParSet

GEN = tp.Union[PDFGenerator, DebyePDFGenerator]


def lattice_to_dict(lattice: SrRealParSet, angunits="rad") -> dict:
    """Convert lattice parameter set to dictionary. If angle is in radian, convert it to degree."""
    dct = dict(zip(lattice.getNames(), lattice.getValues()))
    if angunits == "rad":
        for angle in ('alpha', 'beta', 'gamma'):
            dct[angle] = math.degrees(dct[angle])
    return dct


def atom_to_dict(atom: SrRealParSet) -> dict:
    """Convert atom parameter set to dictionary."""
    dct = dict(zip(atom.getNames(), atom.getValues()))
    dct.update(
        {
            'name': atom.name,
            'element': atom.element
        }
    )
    return dct


def structure_to_dict(phase: SrRealParSet) -> dict:
    """Convert structure parameter set to dictionary."""
    return {
        'lattice': lattice_to_dict(phase.getLattice(), angunits=phase.angunits),
        'atoms': [atom_to_dict(atom) for atom in phase.getScatterers()]
    }


def gather_structures(recipe: FitRecipe) -> tp.Generator:
    """Yield the contribution name, generator name and the dictionary expression of the structure."""
    for con_name, con in recipe.contributions.items():
        genresults = {
            gen_name: structure_to_dict(gen.phase)
            for gen_name, gen in con.generators.items()
        }
        yield con_name, genresults


def conresult_to_dict(result: ContributionResults) -> dict:
    """Convert fit contribution result to dictionary."""
    return {
        'x': result.x.tolist(),
        'y': result.y.tolist(),
        'dy': result.dy.tolist(),
        'ycalc': result.ycalc.tolist(),
        'rw': result.rw,
        'chi2': result.chi2,
        'residual': result.residual
    }


def fitresult_to_dict(result: FitResults) -> dict:
    """Convert fit result to dictionary."""
    return {
        'varnames': result.varnames,
        'varvals': result.varvals,
        'varunc': result.varunc,
        'connames': result.connames,
        'convals': result.convals,
        'conunc': result.conunc,
        'fixednames': result.fixednames,
        'fixedvals': result.fixedvals,
        'cov': result.cov.tolist(),
        'residual': result.residual,
        'penalty': result.penalty,
        'chi2': result.chi2,
        'rchi2': result.rchi2,
        'rw': result.rw,
        'precesion': result.precision,
        'derivstep': result.derivstep,
        'strformat': result.formatResults(),
        'conresults': {
            n: conresult_to_dict(r) for n, r in result.conresults.items()
        }
    }


def recipe_to_dict(recipe: FitRecipe) -> dict:
    """Convert the fit result in recipe to a database friendly dictionary."""
    result = FitResults(recipe)
    doc = fitresult_to_dict(result)
    for con_name, genresults in gather_structures(recipe):
        doc['conresults'][con_name]['genresults'] = genresults
    return doc
