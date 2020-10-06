import typing
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pathlib import Path

import matplotlib.pyplot as plt

from pdfstream.io import load_array
from .io import load_pdfconfig, write_pdfgetter
from .main import get_pdf


def transform(
    cfg_file: str,
    *data_files: str,
    output_dir: str = ".",
    plot_setting: typing.Union[str, dict] = None,
    parallel: bool = False,
    test: bool = False
) -> typing.List[typing.Dict[str, str]]:
    """Transform the data to I(Q), S(Q), F(Q), G(r).

    This is a simple interface for diffpy.pdfgetx. For more interactive usage, please use `pdfgetx3` command.

    Parameters
    ----------
    cfg_file :
        The configure file for diffpy.pdfgetx.

    data_files :
        The single or multiple data files.

    output_dir :
        The output directory for files. The file will be saved in the sub-directories.

    plot_setting :
        The dictionary for the visualization setting. The keys are for the plot in matplotlib
        (https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.plot.html).

    parallel :
        If True, use parallel computing.

    test :
        If True, use test mode (for developers).

    Returns
    -------
    dcts :
        A list of dictionaries. The keys are the output data types and the values are the output file paths.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    if parallel:
        executor = ProcessPoolExecutor() if not test else ThreadPoolExecutor()
        jobs = [
            executor.submit(
                _transform, cfg_file, data_file, output_dir=output_dir, plot_setting=plot_setting, test=test
            )
            for data_file in data_files
        ]
        return [job.result() for job in as_completed(jobs)]
    return [
        _transform(
            cfg_file, data_file, output_dir=output_dir, plot_setting=plot_setting, test=test
        )
        for data_file in data_files
    ]


def _transform(
    cfg_file: str,
    data_file: str,
    output_dir: str = ".",
    plot_setting: typing.Union[str, dict] = None,
    test: bool = False,
) -> typing.Dict[str, str]:
    """Transform the data."""
    pdfconfig = load_pdfconfig(cfg_file)
    chi = load_array(data_file)
    pdfgetter = get_pdf(pdfconfig, chi, plot_setting=plot_setting)
    filename = Path(data_file).stem
    dct = write_pdfgetter(output_dir, filename, pdfgetter)
    if not test:
        plt.show()
    return dct
