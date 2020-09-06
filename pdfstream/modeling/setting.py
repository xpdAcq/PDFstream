"""Set hyper parameters in the recipe."""
import typing as tp

from numpy import ndarray
from diffpy.srfit.fitbase import Profile
from diffpy.srfit.fitbase.parameter import Parameter

from .fitobjs import MyRecipe


def set_range(
        recipe: MyRecipe,
        rmin: tp.Tuple[str, float] = None,
        rmax: tp.Tuple[str, float] = None,
        rstep: tp.Tuple[str, float] = None
) -> MyRecipe:
    """Set fitting range of the single contribution in the recipe.

    Parameters
    ----------
    recipe :
        The recipe. It has only one contribution with profile.

    rmin :
        The minimum value of fitting range (inclusive). If None, keep original value. If "obs", use data value.

    rmax :
        The maximum value of fitting range (inclusive). If None, keep original value. If "obs", use data value.

    rstep :
        The step of fitting range. If None, keep original value. If "obs", use data value.

    Returns
    -------
    recipe :
        The recipe same as the input. Operation is done in place.
    """
    con = next(iter(recipe.contributions.values()))
    con.profile.setCalculationRange(xmin=rmin, xmax=rmax, dx=rstep)
    return recipe


def get_range(recipe: MyRecipe) -> ndarray:
    """Get the fitting range of the single contribution in recipe.

    Parameters
    ----------
    recipe :
        The recipe with a single contribution.

    Returns
    -------
    x :
        The array of the x values in the fitting.
    """
    con = next(iter(recipe.contributions.values()))
    return con.profile.x


def get_variable(recipe: MyRecipe, name: str, ignore: bool = False) -> Parameter:
    """Get a fitting parameter from the recipe."""
    variable = getattr(recipe, name, None)
    if not variable:
        if not ignore:
            raise ValueError("Recipe doesn't have parameter '{}'.".format(name))
    return variable


def set_values(recipe: MyRecipe, values: tp.Dict[str, float], ignore: bool = False) -> MyRecipe:
    """Set the values of fitting parameters in the recipe.

    Parameters
    ----------
    recipe :
        The recipe.

    values :
        The mapping from name of the parameter to its set value.

    ignore :
        If True, ignore the parameter when it is not found in the recipe.

    Returns
    -------
    recipe :
        The input recipe with operation done in place.
    """
    for name, value in values.items():
        variable = get_variable(recipe, name, ignore=ignore)
        if variable:
            variable.setValue(value)
    return recipe


def get_values(recipe: MyRecipe, names: tp.Iterable[str]) -> tp.List[tp.Union[float, None]]:
    """Get the values of the fitting parameters in the recipe.

    Parameters
    ----------
    recipe :
        The recipe.

    names :
        The names of parameters.

    Returns
    -------
    values :
        A list of values in the same order of names. If a value is None, the name is not in the recipe.
    """
    dct = dict(zip(recipe.getNames(), recipe.getValues()))
    return list(map(dct.get, names))


def bound_ranges(
        recipe: MyRecipe, bounds: tp.Dict[str, tp.Union[tp.Tuple, tp.Dict]],
        ignore: bool = False, ratio: bool = False
) -> MyRecipe:
    for name, bound in bounds.items():
        variable = get_variable(recipe, name, ignore=ignore)
        if variable:
            bound_range(variable, bound, ratio=ratio)
    return recipe


def bound_range(variable: Parameter, bound: tp.Union[tp.Tuple, tp.Dict], ratio: bool = False) -> Parameter:
    value = variable.getValue()
    if isinstance(bound, dict):
        if ratio:
            for k, r in bound.items():
                bound[k] = value * r
        variable.boundRange(**bound)
    else:
        if ratio:
            bound = tuple((r * value for r in bound))
        variable.boundRange(*bound)
    return variable


def bound_windows(
        recipe: MyRecipe, bounds: tp.Dict[str, tp.Union[float, tp.Tuple, tp.Dict]],
        ignore: bool = False, ratio: bool = False
) -> MyRecipe:
    for name, bound in bounds.items():
        variable = get_variable(recipe, name, ignore=ignore)
        if variable:
            bound_window(variable, bound, ratio=ratio)
    return recipe


def bound_window(variable: Parameter, bound: tp.Union[float, tp.Tuple, tp.Dict], ratio: bool = False) -> Parameter:
    value = variable.getValue()
    if isinstance(bound, dict):
        if ratio:
            for k, r in bound.items():
                bound[k] = value * r
        variable.boundWindow(**bound)
    elif isinstance(bound, float):
        if ratio:
            bound = bound * value
        variable.boundWindow(bound)
    else:
        if ratio:
            bound = tuple((r * value for r in bound))
        variable.boundWindow(*bound)
    return variable


def get_bounds(recipe: MyRecipe, names: tp.Iterable[str]) -> tp.List[tp.List[float]]:
    dct = dict(zip(recipe.getNames(), recipe.getBounds()))
    return list(map(dct.get, names))
