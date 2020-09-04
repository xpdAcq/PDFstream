"""Create a recipe."""
import inspect
import typing as tp

from diffpy.structure import Structure
from pyobjcryst.crystal import Crystal

from .fitobjs import FunConfig, GenConfig, ConConfig, MyParser

S = tp.Union[Crystal, Structure]


def create(
        name: str,
        data: MyParser,
        equation: str,
        arange: tp.Tuple[float, float, float],
        structures: tp.Dict[str, S],
        functions: tp.Dict[str, tp.Callable],
        ncpu: int = None
):
    genconfigs = [
        GenConfig(
            name=n, structure=s, ncpu=ncpu
        )
        for n, s in structures.items()
    ]
    funconfigs = [
        FunConfig(
            name=n, func=f, argnames=add_suffix(func, name)
        )
        for n, f in functions.items()
    ]
    conconfig = ConConfig(
        name=name, eq=equation, parser=data, fit_range=arange,
        genconfigs=genconfigs, funconfigs=funconfigs
    )
    recipe = make_recipe(conconfig)
    return recipe


def add_suffix(func: tp.Callable, suffix: str) -> tp.List[str]:
    """Add the suffix to the argument names starting at the second the argument. Return the names"""
    args = inspect.getfullargspec(func).args
    return list(
        map(
            lambda arg: '{}_{}'.format(arg, suffix) if arg != "r" else arg,
            args
        )
    )
