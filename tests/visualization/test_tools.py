import matplotlib.pyplot as plt
import numpy as np
import pytest

import pdfstream.visualization.tools as tools


def test_complimentary():
    assert tools.complimentary("black") == "#FFFFFF"


def test_auto_text():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    tools.auto_text("nothing", ax)


@pytest.mark.parametrize(
    "wrong_data",
    [np.zeros((4, 5, 1)), np.zeros((2, 5))]
)
def test_plot_fit_eorr(wrong_data):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    with pytest.raises(ValueError):
        tools.plot_fit(wrong_data, ax=ax)
