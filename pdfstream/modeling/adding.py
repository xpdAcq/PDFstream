"""Add variables to recipe."""
import typing as tp

from diffpy.srfit.pdf import PDFGenerator, DebyePDFGenerator
from diffpy.srfit.structure.objcrystparset import ObjCrystAtomParSet

from .fitobjs import MyRecipe

G = tp.Union[PDFGenerator, DebyePDFGenerator]


def add(
        recipe: MyRecipe,
        names: tp.Tuple[str, str] = None,
        scale: bool = True,
        delta: tp.Union[str, None] = "2",
        lat: tp.Union[str, None] = "s",
        adp: tp.Union[str, None] = "a",
        xyz: tp.Union[str, None] = "s"
) -> None:
    if not names:
        for con_name in recipe.contributions.keys():
            for gen_name in recipe.contributions.keys():
                add(recipe, names=(con_name, gen_name), scale=scale, delta=delta, lat=lat, adp=adp, xyz=xyz)
        return
    gen = getattr(getattr(recipe, names[0]), names[1])
    add_scale(recipe, gen, scale)
    add_delta(recipe, gen, delta)
    add_lat(recipe, gen, lat)
    add_adp(recipe, gen, adp)
    add_xyz(recipe, gen, xyz)
    return


def add_scale(recipe: MyRecipe, gen: G, scale: bool = True) -> None:
    if not scale:
        return
    recipe.addVar(
        gen.scale,
        value=0.,
        name="scale_{}".format(gen.name),
        tag="scale_{}".format(gen.name)
    ).boundRange(
        lb=0.
    )
    return


def add_delta(recipe: MyRecipe, gen: G, delta: tp.Union[str, None]) -> None:
    if not delta:
        return
    if delta == "1":
        par = gen.delta1
    elif delta == "2":
        par = gen.delta2
    else:
        raise ValueError("Unknown delta: {}. Allowed: delta1, delta2.".format(delta))
    recipe.addVar(
        par,
        value=0.,
        name="{}_{}".format(par.name, gen.name),
        tags=["delta_{}".format(gen.name), "delta", gen.name]
    ).boundRange(
        lb=0.
    )
    return


def add_lat(recipe: MyRecipe, gen: G, lat: tp.Union[str, None]) -> None:
    if not lat:
        return
    if lat == "s":
        pars = gen.phase.sgpars.latpars
    elif lat == "a":
        pars = gen.phase.getLattice()
    else:
        raise ValueError("Unknown lat: {}. Allowed: sg, all.".format(lat))
    for par in pars:
        recipe.addVar(
            par, tags=["lat", gen.name, "lat_{}".format(gen.name)]
        ).boundRange(
            lb=0.
        )
    return


def add_adp(recipe: MyRecipe, gen: G, adp: tp.Union[str, None]) -> None:
    if not adp:
        return
    atoms = gen.phase.getScatterers()
    if adp == "e":
        elements = set((atom.element for atom in atoms))
        dct = dict()
        for element in elements:
            dct[element] = recipe.newVar(
                f"Biso_{only_alpha(element)}_{gen.name}",
                value=0.05,
                tags=["adp", gen.name, "adp_{}".format(gen.name)]
            )
        for atom in atoms:
            recipe.constrain(atom.Biso, adp[atom.element])
        return
    if adp == "a":
        pars = [atom.Biso for atom in atoms]
        names = ["Biso_{}".format(atom.name) for atom in atoms]
    elif adp == "s":
        pars = gen.phase.sgpars.adppars
        names = [rename_by_atom(par.name, atoms) for par in pars]
    else:
        raise ValueError("Unknown adp: {}. Allowed: element, sg, all.".format(adp))
    for par, name in zip(pars, names):
        recipe.addVar(
            par,
            name="{}_{}".format(name, gen.name),
            value=par.value if par.value != 0. else 0.05,
            tags=["adp", gen.name, "adp_{}".format(gen.name)]
        ).boundRange(
            lb=0.
        )
    return


def add_xyz(recipe: MyRecipe, gen: G, xyz: tp.Union[str, None]) -> None:
    if not xyz:
        return
    atoms = gen.phase.getScatterers()
    if xyz == "s":
        pars = gen.phase.sgpars.xyzpars
        names = [rename_by_atom(par.name, atoms) for par in pars]
    elif xyz == "a":
        pars, names = list(), list()
        for atom in atoms:
            pars.append(atom.x)
            names.append("x_{}".format(atom.name))
            pars.append(atom.y)
            names.append("y_{}".format(atom.name))
            pars.append(atom.z)
            names.append("z_{}".format(atom.name))
    else:
        raise ValueError("Unknown xyz: {}. Allowed: s, a.".format(adp))
    for par, name in zip(pars, names):
        recipe.addVar(
            par,
            name="{}_{}".format(name, gen.name),
            tags=["xyz", gen.name, "xyz_{}".format(gen.name)]
        )
    return


def rename_by_atom(name: str, atoms: tp.List[ObjCrystAtomParSet]) -> str:
    parts = name.split("_")
    if len(parts) > 1 and parts[1].isdigit() and -1 < int(parts[1]) < len(atoms):
        parts[1] = atoms[int(parts[1])].name
    return "_".join(parts)
