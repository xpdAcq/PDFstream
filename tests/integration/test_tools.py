import numpy as np
import pytest

import pdfstream.integration.tools as tools


def test_bg_sub_error():
    with pytest.raises(ValueError):
        tools.bg_sub(np.ones((2, 2)), np.zeros((3, 3)))
