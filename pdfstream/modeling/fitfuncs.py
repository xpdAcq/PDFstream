import multiprocessing
import os
from datetime import datetime
from typing import Tuple, Union, List, Dict
from uuid import uuid4

import diffpy.srfit.pdf.characteristicfunctions as F
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from diffpy.srfit.fitbase import Profile, FitContribution, FitResults
from diffpy.srfit.fitbase.parameter import ParameterProxy
from diffpy.srfit.pdf import PDFGenerator, DebyePDFGenerator
from diffpy.srfit.structure.sgconstraints import constrainAsSpaceGroup
from matplotlib.axes import Axes
from scipy.optimize import least_squares

from pdfstream.modeling.fitobjs import *
from pdfstream.visualization.main import visualize

__all__ = [
    'make_profile',
    'make_generator',
    'make_recipe',
    'fit',
    'gen_save_all',
    'F',
    'plot',
    'constrainAsSpaceGroup',
    'load_default',
    'sgconstrain',
    'cfconstrain',
    'sgconstrain_all']


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


def _make_df(recipe: MyRecipe) -> Tuple[pd.DataFrame, FitResults]:
    """

    :param recipe: fit recipe.
    :return:
    """
    df = pd.DataFrame()
    res = FitResults(recipe)
    df["name"] = ["Rw", "half_chi2", "penalty"] + res.varnames
    df["val"] = [res.rw, res.chi2 / 2, res.penalty] + res.varvals.tolist()
    df["std"] = [np.nan, np.nan, np.nan] + res.varunc
    df = df.set_index("name")
    return df, res


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
    ax = visualize(data, ax=ax, mode='fit', text=contribution.name)
    plt.show(block=False)
    return ax


def save_csv(recipe: MyRecipe, base_name: str) -> Tuple[str, dict]:
    """
    Save fitting results to a csv file.

    Parameters
    ----------
    recipe : MyRecipe
        The fit recipe.

    base_name : str
        The base name for saving. The saving name will be "{base_name}.csv"

    Returns
    -------
    csv_file : str
        The path to the csv file.

    goodness : dict
        The metric of the goodness of the fit.
    """
    df, res = _make_df(recipe)
    csv_file = rf"{base_name}.csv"
    df.to_csv(csv_file)

    goodness = {
        'rw': res.rw,
        'half_chi2': res.chi2 / 2,
        'penalty': res.penalty
    }
    return csv_file, goodness


def save_fgr(contribution: FitContribution, base_name: str, rw: float) -> str:
    """
    Save fitted PDFs to a four columns txt files with Rw as header.

    Parameters
    ----------
    contribution
        arbitrary number of Fitcontributions.

    base_name
        base name for saving. The saving name will be "{base_name}_{contribution.name}.fgr"

    rw
        value of Rw. It will be in the header as "Rw = {rw}".

    Returns
    -------
    fgr_file : str
        the path to the fgr file.
    """
    fgr_file = rf"{base_name}_{contribution.name}.fgr"
    contribution.profile.savetxt(fgr_file, header=f"Rw = {rw}\nx ycalc y dy")
    return fgr_file


def calc_pgar(contribution: FitContribution, base_name: str, partial_eqs: Dict[str, str] = None) -> str:
    """
    Calculate the partial PDF.

    Parameters
    ----------
    contribution
        The FitContribution to calculate the partial PDF.
    base_name
        The base name for the saving file.
    partial_eqs
        The mapping from the phase name to their equation.

    Returns
    -------
    pgr_file
        The path to the partial pdf data file. It is a multi-column data file with header.
    """
    data = [contribution.profile.x]
    columns = ["r"]
    for phase_name, equation in partial_eqs.items():
        ycalc = contribution.evaluateEquation(equation)
        data.append(ycalc)
        columns.append(phase_name)
    data_array = np.column_stack(data)
    header = " ".join(columns)
    pgr_file = f"{base_name}_{contribution.name}.pgr"
    np.savetxt(pgr_file, data_array, fmt="%.8e", header=header)
    return pgr_file


def save_cif(generator: Union[PDFGenerator, DebyePDFGenerator], base_name: str, con_name: str,
             ext: str = "cif") -> str:
    """
    Save refined structure.

    Parameters
    ----------
    generator
        a ProfileGenerator. The structure is inside the "stru" attribute in it.
    base_name
        base name for saving. The saving name will be "{base_name}_{con_name}_{generator.name}."
    con_name
        name of the contribution that the generators belong to.
    ext
        extension of the structure file. It will also determine the structure file type. Default "cif". Only works
        for diffpy structure.
    Returns
    -------
        the path to the cif or xyz files.
    """
    stru_file = rf"{base_name}_{con_name}_{generator.name}.{ext}"
    stru = generator.stru
    try:
        stru.write(stru_file, ext)
    except AttributeError:
        try:
            with open(stru_file, "w") as f:
                stru.CIFOutput(f)
        except AttributeError:
            raise Warning("Fail to save the structure.")
    return stru_file


def gen_save_all(folder: str, csv: str, fgr: str, cif: str):
    """
    Generate the function save_all to save results of recipes. The database of csv, fgr and cif will be passed to the
    "_save_all" function. If there is no such file, it will be created as an empty csv file.

    Parameters
    ----------
    folder
            folder
        Folder to save the files.
    csv
        The path to the csv file containing fitting results information.
    fgr
        The path to the csv file containing fitted PDFs information.
    cif
        The path to the csv file containing refined structure information.

    Returns
    -------
    save_all
        A function to save results.

    """
    for filepath in (csv, fgr, cif):
        if not os.path.isfile(filepath):
            pd.DataFrame().to_csv(filepath)

    def save_all(recipe: MyRecipe):
        """
        Save fitting results, fitted PDFs and refined structures to files in one folder and save information in
        DataFrames. The DataFrame will contain columns: 'file' (file paths), 'rw' (Rw value) and other information in
        info.

        Parameters
        ----------
        recipe
            The FitRecipe.
        """
        return _save_all(recipe, folder, csv, fgr, cif)

    return save_all


def _save_all(recipe: MyRecipe, folder: str, csv: str, fgr: str, cif: str) -> None:
    """
    Save fitting results, fitted PDFs and refined structures to files in one folder and save information in DataFrames.
    The DataFrame will contain columns: 'file' (file paths), 'rw' (Rw value) and other information in info.

    Parameters
    ----------
    recipe
        Refined recipe to save.
    folder
        Folder to save the files.
    csv
        The path to the csv file containing fitting results information.
    fgr
        The path to the csv file containing fitted PDFs information.
    cif
        The path to the csv file containing refined structure information.
    """
    print(f"Save {recipe.name} ...\n")
    uid = str(uuid4())[:4]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = os.path.join(folder, f"{timestamp}_{uid}")

    csv_file, goodness = save_csv(recipe, name)
    params = ", ".join(recipe.getNames())
    csv_info = dict(recipe_name=recipe.name, **goodness, timestamp=timestamp, csv_file=csv_file,
                    params=params)
    recipe_id = update(csv, csv_info, id_col='recipe_id')

    for con_config in recipe.configs:
        con = getattr(recipe, con_config.name)
        fgr_file = save_fgr(con, base_name=name, rw=goodness.get('rw', 'unknown'))
        config_info = con_config.to_dict()
        if con_config.partial_eqs is not None:
            pgr_file = calc_pgar(con, name, con_config.partial_eqs)
        else:
            pgr_file = None
        fgr_info = dict(recipe_id=recipe_id, **config_info, fgr_file=fgr_file, pgr_file=pgr_file)
        con_id = update(fgr, fgr_info, id_col='con_id')

        for gen_config in con_config.genconfigs:
            gen = getattr(con, gen_config.name)
            cif_file = save_cif(gen, base_name=name, con_name=con_config.name)
            gconfig_info = gen_config.to_dict()
            cif_info = dict(con_id=con_id, recipe_id=recipe_id, **gconfig_info, cif_file=cif_file)
            update(cif, cif_info, id_col='gen_id')
    return


def update(file_path: str, info_dct: dict, id_col: str) -> int:
    """
    Update the database file (a csv file) by appending the information as a row at the end of the dataframe and return
    a serial id of for the piece of information.

    Parameters
    ----------
    file_path
        The path to the csv file that stores the information.
    info_dct
        The dictionary of information.
    id_col
        The column name of the id.

    Returns
    -------
    id_val
        An id for the information.
    """
    df = pd.read_csv(file_path)
    row_dct = {id_col: df.shape[0]}
    row_dct.update(**info_dct)
    if df.empty:
        newdf = pd.DataFrame([row_dct])
    else:
        newdf = df.append(row_dct, ignore_index=True, sort=False)
    newdf.to_csv(file_path, index=False)
    return row_dct[id_col]


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


def cfconstrain(recipe: MyRecipe, fun_name: str, dv: Dict[str, float] = None, con_name: str = None) \
        -> Dict[str, ParameterProxy]:
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

    Returns
    -------
    variables
        The dictionary mapping from the name of the variable to the variable itself.
    """
    variables = {}
    if dv is None:
        _dv = {}
    elif isinstance(dv, str):
        _dv = load_default(dv)
    else:
        _dv = dv

    conconfig = get_conconfig(recipe, con_name)
    con = getattr(recipe, conconfig.name)
    funconfig = get_funconfig(conconfig, fun_name)
    for par_name in funconfig.argnames[1:]:
        par = getattr(con, par_name)
        variables[par_name] = recipe.addVar(par, value=_dv.get(par_name, 100.), tag="cf").boundRange(0, np.inf)
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
    # the default of variables
    if dv is None:
        _dv = {}
    elif isinstance(dv, str):
        _dv = load_default(dv)
    else:
        _dv = dv
    if sg is None:
        sg = 'P1'
    # the bounds
    if bounds is None:
        bounds = {}
    # get FitContribution and PDFGenerator
    con_config = get_conconfig(recipe, con_name)
    gen_config = get_genconfig(con_config, gen_name)
    con = getattr(recipe, con_config.name)
    gen = getattr(con, gen_config.name)
    # initiate variables
    variables = {}
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
    """Use space group to constrain all the generators in the recipe.

    This method is only applicable to the generators initiated by objects in pyobjcryst. It does not work for
    Structure in diffpy.structure.

    Parameters
    ----------
    recipe
        The recipe to add variables.

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

    add_xyz
        Whether to constrain xyz coordinates. Default False.

    Returns
    -------
    variables
        The dictionary mapping from the name of the variable to the variable itself.
    """
    variables = dict()
    for conconfig in recipe.configs:
        for genconfig in conconfig.genconfigs:
            variables.update(
                sgconstrain(recipe, genconfig.name, dv=dv, bounds=bounds, add_xyz=add_xyz)
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
