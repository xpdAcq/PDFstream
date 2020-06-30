import inspect
import types
import typing

from diffpy.srfit.fitbase import FitResults
from matplotlib.axes import Axes
from pyobjcryst.crystal import Crystal

from pdfstream.modeling.fitfuncs import *
from pdfstream.modeling.fitobjs import *

__all__ = [
    'multi_phase',
    'optimize',
    'GenConfig',
    'ConConfig',
    'MyParser',
    'MyRecipe',
    'report',
    'view_fits',
    'fit_calib',
    'FIT_RANGE'
]
FIT_RANGE = typing.Tuple[float, float, float]


def fit_calib(stru: Crystal, data: MyParser, fit_range: FIT_RANGE, ncpu: int = None) -> \
        MyRecipe:
    """The fit the pdf of the calibration. Get the qdamp and qbraod.

    Parameters
    ----------
    stru : Crystal
        The structure of calibration material.

    data : MyParser
        The parser that contains the pdf data.

    fit_range : tuple
        The rmin, rmax and rstep in the unit of angstrom.

    ncpu : int
        The number of cpu used in parallel computing. If None, no parallel computing.

    Returns
    -------
    recipe : MyRecipe
        The refined recipe.
    """
    recipe = multi_phase([stru], data, fit_range, ncpu=ncpu)
    gen = recipe.multi_phase.G0  # gen: PDFGenerator
    recipe.addVar(gen.qdamp, tag='qparams')
    recipe.addVar(gen.qbroad, tag='qparams')
    optimize(
        recipe,
        tags=['scale_G0', 'lat_G0', 'adp_G0', 'delta2_G0', 'qparams'],
        verbose=0
    )
    report(recipe)
    view_fits(recipe)
    return recipe


def _add_suffix(func: types.CodeType, suffix: str):
    """Add the suffix to the argument names starting at the second the argument. Return the names"""
    args = inspect.getargs(func).args
    if len(args) < 2:
        raise ValueError('The function should have at least two arguments.')
    return [args[0]] + ['{}_{}'.format(arg, suffix) for arg in args]


def multi_phase(phases: typing.Iterable[typing.Union[typing.Tuple[types.CodeType, Crystal], Crystal]],
                data: MyParser,
                fit_range: typing.Tuple[float, float, float],
                default_value: dict = None,
                bounds: dict = None,
                add_xyz: bool = False,
                ncpu: int = None) -> MyRecipe:
    """Make the recipe of a multiphase crystal pdf refinement.

    The parameters are taged as 'scale', 'delta2', 'lat', 'adp', 'xyz' (optional) with the suffix
    '_{the name of the generator}'. The unit depends on the structure loaded in the generator.

    Parameters
    ----------
    phases : Iterable.
        An iterable of structures or tuple of characteristic function and structure. The structure is the Crystal.

    data : MyParser
        A parser with parsed data.

    fit_range : tuple
        The rmin, rmax and rstep in the unit of angstrom.

    ncpu : int
        The number of cpu used in parallel computing. If None, no parallel computing.

    default_value : dict
        The the dictionary of default values.
        If None, the following values will be used:
        tag     initiate value      range
        scale   0                   (0, inf)
        delta2  0                   (0, inf)
        lat     par.value           (0, 2 * par.value)
        adp     (U) 0.006 (B) 0.16  (0, inf)
        xyz     par.value           None

    bounds : dict
        The mapping from the name of the variable to the bounds.

    add_xyz
        Whether to constrain xyz coordinates. Default False.

    Returns
    -------
    recipe : MyRecipe
        The recipe with symmetrically constrained variables and without refinement.
    """
    genconfigs, funconfigs, eqs = list(), list(), dict()
    for i, phase in enumerate(phases):
        if isinstance(phase, tuple):
            # attenuated structure
            cf, stru = phase
        else:
            # pure crystal structure
            cf, stru = None, phase
        gname = "G{}".format(i)
        genconfigs.append(
            GenConfig(name=gname, structure=stru, ncpu=ncpu)
        )
        eq = gname
        if cf is not None:
            fname = "f{}".format(i)
            funconfigs.append(
                FunConfig(name=fname, func=cf, argnames=_add_suffix(cf, fname))
            )
            eq += " * " + fname
        eqs.update({gname: eq})
    conconfig = ConConfig(name='multi_phase', partial_eqs=eqs, parser=data, fit_range=fit_range,
                          genconfigs=genconfigs)
    recipe = make_recipe(conconfig)
    sgconstrain_all(recipe, dv=default_value, bounds=bounds, add_xyz=add_xyz)
    return recipe


def optimize(recipe: MyRecipe, tags: typing.List[typing.Union[str, typing.Tuple[str, ...]]], **kwargs) -> None:
    """First fix all variables and then free the variables one by one and fit the recipe.

    Parameters
    ----------
    recipe
        The recipe to fit.

    tags
        The tags of variables to free. It can be single tag or a tuple of tags.

    kwargs
        The kwargs of the 'fit'.
    """
    print(f"Start {recipe.name} with all parameters fixed.")
    recipe.fix('all')
    for n, tag in enumerate(tags):
        if isinstance(tag, tuple):
            print("Free " + ', '.join(tag) + ' ...')
            recipe.free(*tag)
        elif isinstance(tag, str):
            print(f"Free {tag} ...")
            recipe.free(tag)
        else:
            raise TypeError(f"Unknown tag type: {type(tag)}")
        fit(recipe, **kwargs)
    return


def report(recipe: MyRecipe) -> FitResults:
    """Print out the fitting result.

    Parameters
    ----------
    recipe : MyRecipe
        The recipe after refinement.

    Returns
    -------
    res : FitResults
        The object contains the fit results.
    """
    res = FitResults(recipe)
    res.printResults()
    return res


def view_fits(recipe: MyRecipe) -> typing.List[Axes]:
    """View the fit curves. Each FitContribution will be a plot.

    Parameters
    ----------
    recipe : MyRecipe
        The recipe after refinement.

    Returns
    -------
    axes : a list of Axes
        The plots of the fits.
    """
    axes = []
    for conconfig in recipe.configs:
        con = getattr(recipe, conconfig.name)
        axes.append(
            plot(con)
        )
    return axes
