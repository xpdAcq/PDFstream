"""Set hyper parameters in the recipe."""
import typing as tp

from diffpy.srfit.fitbase import Profile

from .fitobjs import MyRecipe


def set_range(
        recipe: MyRecipe,
        name: str = None,
        rmin: tp.Tuple[str, float] = None,
        rmax: tp.Tuple[str, float] = None,
        rstep: tp.Tuple[str, float] = None
) -> None:
    """Set fitting range of contributions in the recipe.

    Parameters
    ----------
    recipe :
        The recipe. It containes at least one contribution with profile.

    name :
        The name of the contribution to set fitting range. If None, set all contributions. Default None.

    rmin :
        The minimum value of fitting range. If None, keep original value. If "obs", use data value.

    rmax :
        The maximum value of fitting range. If None, keep original value. If "obs", use data value.

    rstep :
        The step of fitting range. If None, keep original value. If "obs", use data value.
    """
    if not name:
        for con_name in recipe.contributions.keys():
            set_range(recipe, con_name, rmin, rmax, rstep)
        return
    con = recipe.contributions[name]
    profile: Profile = con.profile
    profile.setCalculationRange(xmin=rmin, xmax=rmax, dx=rstep)
    return
