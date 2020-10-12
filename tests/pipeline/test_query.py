import pytest

import pdfstream.pipeline.query as query


@pytest.mark.parametrize(
    "poni_file",
    [None, "Ni_poni_file"]
)
def test_query_ai(run0, test_data, poni_file):
    ai = query.query_ai(run0.metadata['start'], poni_file=test_data.get(poni_file, None))
    print(ai)
