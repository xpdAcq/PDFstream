import time

from bluesky.callbacks import CallbackBase

try:
    from diffpy.pdfgetx import PDFConfig, PDFGetter
except ImportError:
    pass


class StartStopCallback(CallbackBase):
    """Print the time for analysis"""

    def __init__(self):
        super().__init__()
        self.t0 = 0

    def start(self, doc):
        self.t0 = time.time()
        print("START ANALYSIS ON {}".format(doc["uid"]))

    def stop(self, doc):
        print("FINISH ANALYSIS ON {}".format(doc.get("run_start", "NA")))
        print("Analysis time {}".format(time.time() - self.t0))
