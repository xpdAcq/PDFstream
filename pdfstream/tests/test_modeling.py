from pdfstream.modeling.main import *


def test_multi_phase(db):
    data = {
        'data_id': 0,
        'data_file': db['Ni_gr_file'],
        'qparams': (.04, .02),
    }
    recipe = multi_phase([db['Ni_stru']], data, fit_range=(2., 8., .1))
    optimize(recipe, ['all'])
    report(recipe)
    view(recipe)
