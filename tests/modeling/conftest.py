import pytest
from diffpy.srfit.pdf import characteristicfunctions as F
from diffpy.structure import loadStructure
from pyobjcryst import loadCrystal

from pdfstream.modeling.fitobjs import MyParser
from pdfstream.modeling.main import multi_phase
from tests.conftest import NI_GR, NI_CIF


@pytest.fixture(scope="function", params=[loadCrystal, loadStructure])
def recipe(request):
    parser = MyParser()
    parser.parseFile(NI_GR)
    stru = request.param(NI_CIF)
    recipe = multi_phase([(F.sphericalCF, stru)], parser, fit_range=(2., 8.0, .1), values={
        'psize_G0': 200}, sg_params={'G0': 225})
    return recipe
