import pytest
from diffpy.structure import loadStructure
from pyobjcryst import loadCrystal

from pdfstream.modeling.fitobjs import MyParser
from pdfstream.modeling.main import multi_phase, optimize


@pytest.fixture(scope="module")
def recipes(db):
    """A recipe of crystal in pyobjcryst."""
    parser = MyParser()
    parser.parseFile(db['Ni_gr_file'])
    # a recipe of crystal in pyobjcryst
    phases0 = [loadCrystal(db['Ni_stru_file'])]
    recipe0 = multi_phase(phases0, parser, fit_range=(3., 8., .2))
    optimize(recipe0, ['all'], verbose=0)
    # a recipe of structure in diffpy.structure
    phases1 = [loadStructure(db['Ni_stru_file'])]
    recipe1 = multi_phase(phases1, parser, fit_range=(3., 8., .2), sg_params={'G0': 225})
    optimize(recipe1, ['all'], verbose=0)
    return {
        'pyobjcryst': recipe0,
        'diffpy': recipe1
    }
