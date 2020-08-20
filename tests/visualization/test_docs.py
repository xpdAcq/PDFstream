import matplotlib.pyplot as plt
import numpy as np
import pytest

from pdfstream.visualization.docs import fitted_curves

x = np.linspace(0, np.pi, 100)


@pytest.mark.parametrize(
    "docs",
    [
        [
            {"conresults": [
                {"x": x, "ycalc": np.sin(x), "y": np.sin(x), "rw": 0.0}
            ]},
            {"conresults": [
                {"x": x, "ycalc": np.cos(x), "y": np.cos(x), "rw": 0.0}
            ]}
        ]
    ]
)
def test_fitted_curves(docs):
    fitted_curves(docs)
    plt.show()
    plt.close()
