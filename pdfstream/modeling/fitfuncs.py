import multiprocessing
from typing import Tuple, Union, List, Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from diffpy.srfit.fitbase import Profile, FitContribution
from diffpy.srfit.fitbase.parameter import ParameterProxy
from diffpy.srfit.pdf import PDFGenerator, DebyePDFGenerator
from diffpy.srfit.structure.sgconstraints import constrainAsSpaceGroup
from matplotlib.axes import Axes
from scipy.optimize import least_squares

from pdfstream.modeling.fitobjs import MyParser, MyRecipe, ConConfig, FunConfig, GenConfig
from pdfstream.visualization.main import visualize

__all__ = [
    'make_profile',
    'make_generator',
    'make_recipe',
    'fit',
    'plot',
    'constrainAsSpaceGroup',
    'load_default',
    'sgconstrain',
    'cfconstrain',
    'sgconstrain_all',
    'cfconstrain_all'
]


# functions used in fitting
def make_profile(parser: MyParser, fit_range: Tuple[float, float, float]) -> Profile:
    """
    Make a Profile, parse data file to it and set its calculation range.

    Parameters
    ----------
    parser
        The parser with parsed data from the data source.

    fit_range
        The tuple of (rmax, rmin, dr) in Angstrom.

    Returns
    -------
    profile
        The Profile with the parsed data and the calculation range.
    """
    profile = Profile()
    profile.loadParsedData(parser)
    rmin, rmax, rstep = fit_range
    profile.setCalculationRange(rmin, rmax, rstep)
    return profile


def make_generator(genconfig: GenConfig) -> Union[PDFGenerator, DebyePDFGenerator]:
    """
    Build a generator according to the information in the GenConfig.

    Parameters
    ----------
    genconfig : GenConfig
        A configuration instance for generator building.

    Returns
    -------
    generator: PDFGenerator or DebyePDFGenerator
        A generator built from GenConfig.
    """
    generator = DebyePDFGenerator(genconfig.name) if genconfig.debye else PDFGenerator(genconfig.name)
    generator.setStructure(genconfig.structure, periodic=genconfig.structure)
    ncpu = genconfig.ncpu
    if ncpu:
        pool = multiprocessing.Pool(ncpu)
        generator.parallel(ncpu, mapfunc=pool.imap_unordered)
    return generator


def make_contribution(conconfig: ConConfig) -> FitContribution:
    """
    Make a FitContribution according to the ConConfig.

    Parameters
    ----------
    conconfig : ConConfig
        The configuration instance for the FitContribution.

    Returns
    -------
    contribution : FitContribution
        The FitContribution built from ConConfig.
    """
    contribution = FitContribution(conconfig.name)

    fit_range = conconfig.fit_range
    profile = make_profile(conconfig.parser, fit_range)
    contribution.setProfile(profile, xname="r")

    for genconfig in conconfig.genconfigs:
        generator = make_generator(genconfig)
        if conconfig.qparams is not None:
            generator.qdamp.value = conconfig.qparams[0]
            generator.qbroad.value = conconfig.qparams[1]
        contribution.addProfileGenerator(generator)

    for base_line in conconfig.baselines:
        contribution.addProfileGenerator(base_line)

    for function in conconfig.funconfigs:
        name = function.name
        func_type = function.func
        argnames = function.argnames
        contribution.registerFunction(func_type, name, argnames)

    contribution.setEquation(conconfig.eq)
    contribution.setResidualEquation(conconfig.res_eq)

    return contribution


def make_recipe(*conconfigs: ConConfig) -> MyRecipe:
    """
    Make a FitRecipe based on single or multiple ConConfig.

    Parameters
    ----------
    conconfigs
        The configurations of single or multiple FitContribution.

    Returns
    -------
    recipe
        MyRecipe built from ConConfigs.
    """
    recipe = MyRecipe(configs=conconfigs)

    for conconfig in conconfigs:
        contribution = make_contribution(conconfig)
        recipe.addContribution(contribution, conconfig.weight)

    recipe.fithooks[0].verbose = 0

    return recipe


def fit(recipe: MyRecipe, **kwargs) -> None:
    """
    Fit the data according to recipe. parameters associated with fitting can be set in kwargs.

    Parameters
    ----------
    recipe
        MyRecipe to fit.

    kwargs
        Parameters in fitting. They are
            verbose: how much information to print. Default 1.
            values: initial value for fitting. Default get from recipe.
            bounds: two list of lower and upper bounds. Default get from recipe.
            xtol, gtol, ftol: tolerance in least squares. Default 1.E-5, 1.E-5, 1.E-5.
            max_nfev: maximum number of evaluation of residual function. Default None.
    """
    values = kwargs.get("values", recipe.values)
    bounds = kwargs.get("bounds", recipe.getBounds2())
    verbose = kwargs.get("verbose", 1)
    xtol = kwargs.get("xtol", 1.E-5)
    gtol = kwargs.get("gtol", 1.E-5)
    ftol = kwargs.get("ftol", 1.E-5)
    max_nfev = kwargs.get("max_fev", None)
    least_squares(recipe.residual, values, bounds=bounds, verbose=verbose, xtol=xtol, gtol=gtol, ftol=ftol,
                  max_nfev=max_nfev)
    return


def plot(contribution: FitContribution) -> Axes:
    """
    Plot the fits for all FitContributions in the recipe.

    Parameters
    ----------
    contribution : FitContribution
        The FitRecipe.

    Returns
    -------
    ax : Axes
        The axes that has the plot.
    """
    r = contribution.profile.x
    g = contribution.profile.y
    gcalc = contribution.profile.ycalc
    gdiff = g - gcalc
    data = np.stack([r, g, gcalc, gdiff])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax = visualize(data, ax=ax, mode='fit', legend=contribution.name)
    plt.show(block=False)
    return ax


def load_default(csv_file: str):
    """
    Load the default value as a dictionary from the csv file of fitting results.

    Parameters
    ----------
    csv_file
        The path to the csv file.

    Returns
    -------
    default_val_dict
        A dictionary of variable names and its default values.
    """
    default_val_dict = pd.read_csv(csv_file, index_col=0)['val'].to_dict()
    return default_val_dict


def cfconstrain(recipe: MyRecipe, fun_name: str, dv: Dict[str, float] = None, bounds: Dict[str, tuple] = None,
                con_name: str = None) -> Dict[str, ParameterProxy]:
    """
    Add parameters in the Characteristic functions in the FitContribution into the MyRecipe.
    Return the added variables in a dictionary.

    Parameters
    ----------
    recipe
        The recipe to add the parameters

    fun_name
        The name of the characteristic function.

    dv
        The path to the .csv file contains the fitting results or the dictionary of values.
        If None, use 100 A for any parameters as default value.

    con_name
        The name of the FitContribution where the parameters are. If None, use the first one in the recipe.

    bounds
        The mapping from the name of the variable to the tuple of bounds (min, max). Defulat (0, +inf).

    Returns
    -------
    variables
        The dictionary mapping from the name of the variable to the variable itself.
    """
    variables = dict()
    if dv is None:
        _dv = dict()
    elif isinstance(dv, str):
        _dv = load_default(dv)
    else:
        _dv = dv
    if bounds is None:
        bounds = dict()

    conconfig = get_conconfig(recipe, con_name)
    con = getattr(recipe, conconfig.name)
    funconfig = get_funconfig(conconfig, fun_name)
    for par_name in funconfig.argnames[1:]:
        par = getattr(con, par_name)
        variables[par_name] = recipe.addVar(par, value=_dv.get(par_name, 100.), tag="cf").boundRange(
            *bounds.get(par_name, (0, np.inf)))
    return variables


def sgconstrain(recipe: MyRecipe, gen_name: str = None, con_name: str = None, sg: Union[int, str] = None,
                dv: Union[str, Dict[str, float]] = None, bounds: Dict[str, tuple] = None,
                scatterers: List = None, add_xyz=False) \
        -> Dict[str, ParameterProxy]:
    """Constrain the generator by space group. The constrained parameters are scale, delta2, lattice parameters,
    ADPs and xyz coordinates. The lattice constants and xyz coordinates are constrained by space group while the
    ADPs are constrained by elements. All paramters will be added as '{par.name}_{gen.name}'. The parameters
    tags are scale_{gen.name}, delta2_{gen.name}, lat_{gen.name}, adp_{gen.name}, xyz_{gen.name}. Return the
    added variables in a dictionary.

    Parameters
    ----------
    recipe
        The recipe to add variables.

    gen_name
        The name of the PDFGenerator to constrain.

    con_name
        The name of the FitContribution where the PDFGenerator is in. If None, get it according to the name of
        the first ConConfig in 'recipe.configs'. Default None.

    sg
        The space group. The expression can be the string. If the structure is Crystal object, use internal
        constrain. If not, use the space group read by the gen_config.

    dv
        The path to the .csv file contains the fitting results or the dictionary of values.
        If None, the following values will be used:
        type, initiate value, range, tag
        scale, 0, (0, inf), scale_{gen.name}
        delta2, 0, (0, inf), delta2_{gen.name}
        lat, par.value, (0, 2 * par.value), lat_{gen.name}
        adp, 0.006, (0, inf), adp_{gen.name}
        xyz, par.value, None, xyz_{gen.name}

    bounds
        The mapping from the name of the variable to the tuple of the arguments for the bounding function.

    scatterers
        The argument scatters of the constrainAsSpaceGroup. If None, None will be used.

    add_xyz
        Whether to constrain xyz coordinates. Default False.

    Returns
    -------
    variables
        The dictionary mapping from the name of the variable to the variable itself.
    """
    # initiate variables
    variables = dict()
    # the default of variables
    if dv is None:
        _dv = dict()
    elif isinstance(dv, str):
        _dv = load_default(dv)
    else:
        _dv = dv
    if sg is None:
        sg = 'P1'
    # the bounds
    if bounds is None:
        bounds = dict()
    # get FitContribution and PDFGenerator
    con_config = get_conconfig(recipe, con_name)
    gen_config = get_genconfig(con_config, gen_name)
    con = getattr(recipe, con_config.name)
    gen = getattr(con, gen_config.name)
    # add scale
    name = f'scale_{gen.name}'
    variables[name] = recipe.addVar(gen.scale, name=name, value=_dv.get(name, 0.)).boundRange(
        *bounds.get(name, (0., np.inf)))
    # add delta2
    name = f'delta2_{gen.name}'
    variables[name] = recipe.addVar(gen.delta2, name=name, value=_dv.get(name, 0.)).boundRange(
        *bounds.get(name, (0., np.inf)))
    # constrain by spacegroup
    if gen_config.stru_type == "crystal":
        sgpars = gen.phase.sgpars
        print(f"Constrain '{gen.name}' by space group implicitly.")
    elif gen_config.stru_type == "diffpy":
        sgpars = constrainAsSpaceGroup(gen.phase, sg, constrainadps=False, scatterers=scatterers)
        print(f"Constrain '{gen.name}' by space group '{sg}'.")
    else:
        raise ValueError(f"stru_type '{gen_config.stru_type}' does not allow space group constrain.")
    # add latpars
    for par in sgpars.latpars:
        name = f'{par.name}_{gen.name}'
        variables[name] = recipe.addVar(par, name=name, value=_dv.get(name, par.value),
                                        tag=f'lat_{gen.name}').boundWindow(bounds.get(name, par.value))
    # constrain adps
    atoms = gen.phase.getScatterers()
    elements = set([atom.element for atom in atoms])
    adp = {}
    var_dct = {
        "crystal": ("Biso", 0.16, (0, np.inf)),
        "diffpy": ("Uiso", 0.006, (0, np.inf))
    }
    var_name, init_value, bound_range = var_dct.get(gen_config.stru_type)
    for element in elements:
        name = f'{var_name}_{only_alpha(element)}_{gen.name}'
        variables[name] = adp[element] = recipe.newVar(name, value=_dv.get(name, init_value),
                                                       tag=f'adp_{gen.name}').boundRange(
            *bounds.get(name, bound_range))
    for atom in atoms:
        recipe.constrain(getattr(atom, var_name), adp[atom.element])
    # add xyzpars
    if add_xyz:
        for par in sgpars.xyzpars:
            name = f'{par.name}_{gen.name}'
            variables[name] = recipe.addVar(par, name=name, value=_dv.get(name, par.value),
                                            tag=f'xyz_{gen.name}').boundWindow(
                bounds.get(name, np.inf))
    return variables


def sgconstrain_all(recipe: MyRecipe, dv: dict = None, bounds: dict = None, add_xyz: bool = False):
    """Use space group to constrain all the generators in the recipe. See sgconstrain for details."""
    variables = dict()
    for conconfig in recipe.configs:
        for genconfig in conconfig.genconfigs:
            variables.update(
                sgconstrain(recipe, genconfig.name, dv=dv, bounds=bounds, add_xyz=add_xyz)
            )
    return variables


def cfconstrain_all(recipe: MyRecipe, dv: dict = None, bounds: dict = None):
    """Constrain all the parameters in characteristic functions."""
    variables = dict()
    for conconfig in recipe.configs:
        for funconfig in conconfig.funconfigs:
            variables.update(
                cfconstrain(recipe, funconfig.name, dv=dv, bounds=bounds)
            )
    return variables


def only_alpha(s: str):
    """Remove all characters other than alphabets. Use to get a valid variable name."""
    return ''.join((c for c in s if c.isalpha()))


def get_conconfig(recipe: MyRecipe, con_name: str = None) -> ConConfig:
    """Get the ConConfig from the MyRecipe."""
    if con_name is None:
        return recipe.configs[0]
    for config in recipe.configs:
        if config.name == con_name:
            return config
    else:
        raise ValueError(f"No FitContribution names '{con_name}' in FitRecipe '{recipe.name}'.")


def get_genconfig(con_config: ConConfig, gen_name: str = None) -> GenConfig:
    """Get the GenConfig from the ConConfig."""
    if gen_name is None:
        return con_config.genconfigs[0]
    for genconfig in con_config.genconfigs:
        if genconfig.name == gen_name:
            return genconfig
    else:
        raise ValueError(f"No ProfileGenerator names '{gen_name}' in FitContribution '{con_config.name}'.")


def get_funconfig(con_config: ConConfig, fun_name: str = None) -> FunConfig:
    """Get the FunConfig from the ConConfig."""
    if fun_name is None:
        return con_config.funconfigs[0]
    for funconfig in con_config.funconfigs:
        if funconfig.name == fun_name:
            return funconfig
    else:
        raise ValueError(f"No CharacteristicFunction names '{fun_name}' in FitContribution '{con_config.name}'.")
