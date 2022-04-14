from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from databroker import Broker
from pdfstream.callbacks.analyzer import Analyzer
from pdfstream.callbacks.config import Config
from pdfstream.callbacks.darksubtraction import DarkSubtraction
from pdfstream.callbacks.datakeys import DataKeys


def test_Analyzer(db_with_new_xpdacq: Broker, local_dir: Path):
    """Test if the analyzer can correctly average, integrate and transform
    the dark subtracted image.

    Parameters
    ----------
    db_with_new_xpdacq : Broker
        The databroker that contains a temperature ramping scan.
        The detector data is `pe1_image` and the temperature is `temperature`.
    local_dir : Path
        The local directory to save the dark subtracted image plots.
    """
    db = db_with_new_xpdacq
    run = db[-1]
    dark_subtraction = DarkSubtraction("pe1_image")
    config = Config()
    data_keys = DataKeys("pe1", "pe1_image")
    analyzer = Analyzer(data_keys, config)

    def save(fig: plt.Figure, name: str) -> None:
        filename = name + "_{}.png".format(doc["seq_num"])
        filepath = local_dir.joinpath(filename)
        fig.savefig(filepath)
        return

    def plot_and_save(doc: dict, x: str, y: str, name: str) -> None:
        fig, ax = plt.subplots()
        ax.plot(doc["data"][x], doc["data"][y])
        save(fig, name)
        return

    def show_and_save(doc: dict, image: str, mask: str, name: str) -> None:
        fig, ax = plt.subplots()
        masked_image = np.ma.masked_array(doc["data"][image], doc["data"][mask], copy=False)
        ax.imshow(masked_image, interpolation="none", vmax=6000)
        save(fig, name)
        return

    for name, doc in run.documents(fill="yes"):
        name, doc = dark_subtraction(name, doc)
        name, doc = analyzer(name, doc)
        if (
            name == "event"
        ) and (
            "pe1_image" in doc["data"]
        ) and (
            "temperature" in doc["data"]
        ):
            show_and_save(doc, data_keys.image, data_keys.mask, "masked_image")
            plot_and_save(doc, data_keys.chi_2theta, data_keys.chi_I, "chi_tth")
            plot_and_save(doc, data_keys.chi_Q, data_keys.chi_I, "chi_Q")
            plot_and_save(doc, data_keys.iq_Q, data_keys.iq_I, "iq")
            plot_and_save(doc, data_keys.sq_Q, data_keys.sq_I, "sq")
            plot_and_save(doc, data_keys.fq_Q, data_keys.fq_I, "fq")
            plot_and_save(doc, data_keys.gr_r, data_keys.gr_G, "gr")
    return
