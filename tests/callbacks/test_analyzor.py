from databroker.v2 import Broker
from databroker.core import BlueskyRun
from pdfstream.callbacks.analyzer import Analyzor
from pdfstream.callbacks.config import Config


def test_analyzor(db_with_new_xpdacq: Broker):
    db = db_with_new_xpdacq
    del db_with_new_xpdacq
    config = Config()
    analyzor = Analyzor(config)
    run: BlueskyRun = db[-1]
    for name, doc in run.documents(fill="yes"):
        analyzor(name, doc)
    
