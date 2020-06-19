from typing import *

from diffpy.srfit.fitbase import FitResults
from pdfstream.modeling.fitfuncs import *
from pdfstream.modeling.fitobjs import *
from pyobjcryst.crystal import Crystal

__all__ = [
    'multi_phase',
    'optimize',
    'GenConfig',
    'ConConfig',
    'report',
    'view'
]


def multi_phase(strus: Iterable[Crystal], data: dict, fit_range: Tuple[float, float, float] = (0., 30., 0.01),
                ncpu: int = None) -> MyRecipe:
    """"""
    genconfigs = [
        GenConfig(
            name="phase_{}".format(i),
            structure=stru,
            ncpu=ncpu
        )
        for i, stru in enumerate(strus)
    ]
    eq = ' + '.join([_.name for _ in genconfigs])
    conconfig = ConConfig(name='multi_phase', eq=eq, **data, fit_range=fit_range, genconfigs=genconfigs)
    recipe = make_recipe(conconfig)
    sgconstrain_all(recipe)
    return recipe


def optimize(recipe: MyRecipe, tags: List[Union[str, Tuple[str, ...]]], **kwargs) -> None:
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
    """
    Print out the result of the recipe.

    Parameters
    ----------
    recipe : MyRecipe
        The recipe to print the results.

    Returns
    -------
    res : FitResults
        The object contains the fit results.
    """
    res = FitResults(recipe)
    res.printResults()
    return res


def view(recipe: MyRecipe) -> None:
    """"""
    for conconfig in recipe.configs:
        con = getattr(recipe, conconfig.name)
        plot(con)
    return
