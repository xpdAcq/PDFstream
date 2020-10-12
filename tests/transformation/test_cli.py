from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import pytest

import pdfstream.transformation.cli as cli


@pytest.mark.parametrize(
    "parallel, plot_setting",
    [(False, None), (True, "OFF")]
)
def test_transform(test_data, parallel, plot_setting):
    with TemporaryDirectory() as temp_dir:
        dcts = cli.transform(
            test_data["Ni_gr_file"], test_data["Ni_chi_file"],
            plot_setting=plot_setting, output_dir=temp_dir, parallel=parallel, test=True
        )
        plt.close()
        for dct in dcts:
            for output_file in dct.values():
                assert Path(output_file).is_file()
