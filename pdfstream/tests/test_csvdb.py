import os
from pathlib import Path

import pandas as pd
from pkg_resources import resource_filename

import pdfstream.modeling.csvdb as csvdb


def test_summarize():
    example_file = resource_filename('pdfstream', 'test_data/csvdb_example.csv')
    df = pd.read_csv(example_file)
    cwd = os.getcwd()
    os.chdir(Path(example_file).parent)
    lst = csvdb.summarize(df, output=True)
    os.chdir(cwd)
    assert type(lst[0]) == pd.DataFrame
