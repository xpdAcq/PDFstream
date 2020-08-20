import matplotlib.pyplot as plt
import numpy as np
import pytest

from pdfstream.visualization.docs import fitted_curves

x = np.linspace(0, np.pi, 100)
data = [
    {
        "name": "sine",
        "conresults": [
            {"x": x, "ycalc": np.sin(x), "y": np.sin(x), "rw": 0.0}
        ]
    },
    {
        "name": "cosine",
        "conresults": [
            {"x": x, "ycalc": np.cos(x), "y": np.cos(x), "rw": 0.0}
        ]
    }
]


@pytest.mark.parametrize(
    "docs,text_keys",
    [
        (data, None),
        (data, ("name",))
    ]
)
def test_fitted_curves(docs, text_keys):
    fitted_curves(docs, text_keys=text_keys)
    plt.show()
    plt.close()
