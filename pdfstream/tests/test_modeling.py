import matplotlib.pyplot as plt
import pytest

from pdfstream.modeling.main import MyParser, multi_phase, fit_calib, optimize, F


@pytest.mark.parametrize(
    "data_key,default_value,bounds,free_params,expected",
    [
        (
                "Ni_stru",
                {'scale_G0': 0.1, 'a_G0': 3.42, 'Biso_Ni_G0': 0.07, 'psize_f0': 300, 'delta2_G0': 2.5},
                {'scale_G0': [-1, 1], 'a_G0': [0, 6], 'Biso_Ni_G0': [0, 1],
                 'psize_f0': [2, 400], 'delta2_G0': [0, 5]},
                True,
                {'scale_G0', 'a_G0', 'Biso_Ni_G0', 'psize_f0', 'delta2_G0'}
        ),
        (
                "Ni_stru_diffpy",
                {'scale_G0': 0.1, 'a_G0': 3.42, 'Biso_Ni_G0': 0.07, 'psize_f0': 300, 'delta2_G0': 2.5},
                {'scale_G0': [-1, 1], 'a_G0': [0, 6], 'Biso_Ni_G0': [0, 1],
                 'psize_f0': [2, 400], 'delta2_G0': [0, 5]},
                False,
                {'Biso_Ni_G0', 'a_G0', 'alpha_G0', 'b_G0', 'beta_G0', 'c_G0', 'gamma_G0', 'delta2_G0',
                 'psize_f0', 'scale_G0'}
        ),
        (
                "ZrP_stru",
                None,
                None,
                False,
                {'Biso_O_G0', 'Biso_P_G0', 'Biso_Zr_G0', 'a_G0', 'b_G0', 'beta_G0', 'c_G0',
                 'delta2_G0', 'psize_f0', 'scale_G0'}
        ),
        (
                "ZrP_stru",
                None,
                {'x_0_G0': [-2, 2]},
                True,
                {'Biso_O_G0',
                 'Biso_P_G0',
                 'Biso_Zr_G0',
                 'a_G0',
                 'b_G0',
                 'beta_G0',
                 'c_G0',
                 'delta2_G0',
                 'psize_f0',
                 'scale_G0',
                 'x_0_G0',
                 'x_1_G0',
                 'x_2_G0',
                 'x_3_G0',
                 'x_4_G0',
                 'x_5_G0',
                 'x_6_G0',
                 'x_7_G0',
                 'x_8_G0',
                 'x_9_G0',
                 'y_0_G0',
                 'y_1_G0',
                 'y_2_G0',
                 'y_3_G0',
                 'y_4_G0',
                 'y_5_G0',
                 'y_6_G0',
                 'y_7_G0',
                 'y_8_G0',
                 'y_9_G0',
                 'z_0_G0',
                 'z_1_G0',
                 'z_2_G0',
                 'z_3_G0',
                 'z_4_G0',
                 'z_5_G0',
                 'z_6_G0',
                 'z_7_G0',
                 'z_8_G0',
                 'z_9_G0'}
        )
    ]
)
def test_multi_phase(db, data_key, default_value, bounds, free_params, expected):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    recipe = multi_phase(
        [(F.sphericalCF, db[data_key])], parser,
        fit_range=(2., 8.0, .1),
        default_value=default_value,
        bounds=bounds
    )
    # xyz is added as fixed variables, free them for testing purpose
    if free_params:
        recipe.free("all")
    if expected:
        assert set(recipe.getNames()) == expected
    if default_value:
        actual_values = dict(zip(recipe.getNames(), recipe.getValues()))
        for name, expected_value in default_value.items():
            assert actual_values[name] == expected_value
    if bounds:
        actual_bounds = dict(zip(recipe.getNames(), recipe.getBounds()))
        for name, expected_bound in bounds.items():
            assert actual_bounds[name] == expected_bound


def test_optimize(db):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    recipe = multi_phase([(F.sphericalCF, db['Ni_stru'])], parser, fit_range=(2., 8.0, .1), default_value={
        'psize_G0': 200})
    optimize(recipe, ['all'], xtol=1e-3, gtol=1e-3, ftol=1e-3)


def test_MyParser(db):
    parser = MyParser()
    meta = {'qmin': 1, 'qmax': 24, 'qdamp': 0.04, 'qbroad': 0.02}
    parser.parseDict(db['Ni_gr'], meta=meta)
    recipe = multi_phase([db['Ni_stru']], parser, fit_range=(0., 8., .1))
    con = next(iter(recipe.contributions.values()))
    gen = next(iter(con.generators.values()))
    assert gen.getQmin() == meta['qmin']
    assert gen.getQmax() == meta['qmax']
    assert gen.qdamp.value == meta['qdamp']
    assert gen.qbroad.value == meta['qbroad']


def test_fit_calib(db):
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    fit_calib(db['Ni_stru'], parser, fit_range=(2., 8., .1))
    plt.close()
