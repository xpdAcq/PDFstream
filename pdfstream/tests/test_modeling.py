from tempfile import TemporaryDirectory
import numpy as np

import matplotlib.pyplot as plt
import pytest
from pyobjcryst import loadCrystal

from pdfstream.modeling.main import multi_phase, fit_calib, optimize, F, save
from pdfstream.modeling.fitobjs import map_stype, GenConfig, MyParser, ConConfig


@pytest.mark.parametrize(
    "meta",
    [
        None,
        {'qmin': 1, 'qmax': 24, 'qdamp': 0.04, 'qbroad': 0.02}
    ]
)
def test_MyParser_parseDict(db, meta):
    parser = MyParser()
    parser.parseDict(db['Ni_gr'], meta=meta)
    recipe = multi_phase([db['Ni_stru']], parser, fit_range=(0., 8., .1))
    con = next(iter(recipe.contributions.values()))
    gen = next(iter(con.generators.values()))
    # if meta = None, generator will use the default values
    assert gen.getQmin() == parser._meta.get('qmin', 0.0)
    assert gen.getQmax() == parser._meta.get('qmax', 100. * np.pi)
    assert gen.qdamp.value == parser._meta.get('qdamp', 0.0)
    assert gen.qbroad.value == parser._meta.get('qbroad', 0.0)


@pytest.mark.parametrize(
    "data",
    [
        np.zeros((1, 5)),
        np.zeros((5, 5))
    ]
)
def test_MyParser_parseDict_error(data):
    parser = MyParser()
    with pytest.raises(ValueError):
        parser.parseDict(data)


@pytest.mark.parametrize(
    "data_key",
    ['Ni_pdfgetter']
)
@pytest.mark.parametrize(
    "meta",
    [None, {'qmax': 19}]
)
def test_MyParser_parsePDFGetter(db, data_key, meta):
    pdfgetter = db[data_key]
    parser = MyParser()
    parser.parsePDFGetter(pdfgetter, add_meta=meta)
    if meta:
        for key, value in meta.items():
            assert parser._meta[key] == value


@pytest.mark.parametrize(
    "mode,stype",
    [
        ("xray", "X"),
        ("neutron", "N"),
        ("sas", "X")
    ]
)
def test_map_stype(mode, stype):
    assert map_stype(mode) == stype


def test_map_stype_error():
    with pytest.raises(ValueError):
        map_stype("nray")


@pytest.mark.parametrize(
    "stru_key,expect",
    [
        ("Ni_stru_molecule", (False, True)),
        ("Ni_stru", (True, False)),
        ("Ni_stru_diffpy", (True, False))
    ]
)
def test_GenConfig(db, stru_key, expect):
    # noinspection PyArgumentList
    gen_config = GenConfig("G0", db[stru_key])
    assert gen_config.periodic == expect[0]
    assert gen_config.debye == expect[1]


@pytest.mark.parametrize(
    "kwargs,expect",
    [
        ({'eq': 'G0'}, {'eq': 'G0', 'partial_eqs': None}),
        ({'eq': 'G0', 'partial_eqs': {'Ni': 'G0'}}, {'eq': 'G0', 'partial_eqs': {'Ni': 'G0'}})
    ]
)
def test_ConConfig(db, kwargs, expect):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    stru = db['Ni_stru']
    con_config = ConConfig(
        name="con",
        parser=parser,
        fit_range=(0., 8., .1),
        genconfigs=[GenConfig('G0', stru)],
        **kwargs
    )
    for key, value in expect.items():
        assert getattr(con_config, key) == value


def test_ConConfig_error(db):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    with pytest.raises(ValueError):
        ConConfig(
            name="con",
            parser=parser,
            fit_range=(0., 8., .1),
        )


@pytest.mark.parametrize(
    "data_key,kwargs,free_params,expected",
    [
        (
                "Ni_stru",
                {
                    'values': {'scale_G0': 0.1, 'a_G0': 3.42, 'Biso_Ni_G0': 0.07, 'psize_f0': 300,
                               'delta2_G0': 2.5},
                    'bounds': {'scale_G0': [-1, 1], 'a_G0': [0, 6], 'Biso_Ni_G0': [0, 1], 'psize_f0': [2, 400],
                               'delta2_G0': [0, 5]}
                },
                True,
                {'scale_G0', 'a_G0', 'Biso_Ni_G0', 'psize_f0', 'delta2_G0'}
        ),
        (
                "Ni_stru_diffpy",
                {
                    'values': {'scale_G0': 0.1, 'a_G0': 3.42, 'Biso_Ni_G0': 0.07, 'psize_f0': 300,
                               'delta2_G0': 2.5},
                    'bounds': {'scale_G0': [-1, 1], 'a_G0': [0, 6], 'Biso_Ni_G0': [0, 1], 'psize_f0': [2, 400],
                               'delta2_G0': [0, 5]},
                },
                False,
                {'Biso_Ni_G0', 'a_G0', 'alpha_G0', 'b_G0', 'beta_G0', 'c_G0', 'gamma_G0', 'delta2_G0',
                 'psize_f0', 'scale_G0'}
        ),
        (
                "ZrP_stru",
                dict(),
                False,
                {'Biso_O_G0', 'Biso_P_G0', 'Biso_Zr_G0', 'a_G0', 'b_G0', 'beta_G0', 'c_G0',
                 'delta2_G0', 'psize_f0', 'scale_G0'}
        ),
        (
                "ZrP_stru",
                {
                    'bounds': {'x_0_G0': [-2, 2]}
                },
                True,
                {'Biso_O_G0', 'Biso_P_G0', 'Biso_Zr_G0', 'a_G0', 'b_G0', 'beta_G0', 'c_G0', 'delta2_G0',
                 'psize_f0', 'scale_G0', 'x_0_G0', 'x_1_G0', 'x_2_G0', 'x_3_G0', 'x_4_G0', 'x_5_G0', 'x_6_G0',
                 'x_7_G0', 'x_8_G0', 'x_9_G0', 'y_0_G0', 'y_1_G0', 'y_2_G0', 'y_3_G0', 'y_4_G0',
                 'y_5_G0', 'y_6_G0', 'y_7_G0', 'y_8_G0', 'y_9_G0', 'z_0_G0', 'z_1_G0', 'z_2_G0',
                 'z_3_G0', 'z_4_G0', 'z_5_G0', 'z_6_G0', 'z_7_G0', 'z_8_G0', 'z_9_G0'}
        ),
        (
                "Ni_stru",
                {
                    'cf_params': ['psize_f0'],
                    'sg_params': dict()
                },
                True,
                {'psize_f0'}
        ),
        (
                "Ni_stru_diffpy",
                {
                    'cf_params': list(),
                    'sg_params': {'G0': 225}
                },
                True,
                {'scale_G0', 'a_G0', 'Biso_Ni_G0', 'delta2_G0'}
        )
    ]
)
def test_multi_phase(db, data_key, kwargs, free_params, expected):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    recipe = multi_phase(
        [(F.sphericalCF, db[data_key])], parser,
        fit_range=(2., 8.0, .1),
        **kwargs
    )
    # xyz is added as fixed variables, free them for testing purpose
    if free_params:
        recipe.free("all")
    # check parameters
    if expected:
        assert set(recipe.getNames()) == expected
    # check default values
    values = kwargs.get('values')
    if values:
        actual_values = dict(zip(recipe.getNames(), recipe.getValues()))
        for name, expected_value in values.items():
            assert actual_values[name] == expected_value
    # check bounds
    bounds = kwargs.get('bounds')
    if bounds:
        actual_bounds = dict(zip(recipe.getNames(), recipe.getBounds()))
        for name, expected_bound in bounds.items():
            assert actual_bounds[name] == expected_bound


@pytest.fixture(scope="function")
def recipe(db):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    stru = loadCrystal(db['Ni_stru_file'])
    recipe = multi_phase([(F.sphericalCF, stru)], parser, fit_range=(2., 8.0, .1), values={
        'psize_G0': 200})
    return recipe


def test_optimize(recipe):
    optimize(recipe, ['all'], xtol=1e-2, gtol=1e-2, ftol=1e-2)


@pytest.mark.parametrize(
    "stru_fmt",
    [
        "cif",
        "xyz"
    ]
)
def test_save(recipe, stru_fmt):
    optimize(recipe, ['all'], xtol=1e-3, gtol=1e-3, ftol=1e-3)
    with TemporaryDirectory() as temp_dir:
        res_file, fgr_files, stru_files = save(recipe, base_name="test", folder=temp_dir, stru_fmt=stru_fmt)
        assert res_file.is_file()
        assert len(fgr_files) == 1 and fgr_files[0].is_file()
        assert len(stru_files) == 1 and stru_files[0].is_file()


def test_fit_calib(db):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    fit_calib(db['Ni_stru'], parser, fit_range=(2., 8., .1))
    plt.close()
