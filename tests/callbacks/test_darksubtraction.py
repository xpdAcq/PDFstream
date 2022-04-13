from pathlib import Path

import matplotlib.pyplot as plt
from databroker import Broker
from pdfstream.callbacks.darksubtraction import DarkSubtraction


def test_DarkSubtraction(db_with_new_xpdacq: Broker, local_dir: Path):
    """Test if the dark subtraction can correctly subtract an Ni diffraction image.

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
    count = 0
    for name, doc in run.documents(fill="yes"):
        name, doc = dark_subtraction(name, doc)
        if (
            name == "event"
        ) and (
            "pe1_image" in doc["data"]
        ) and (
            "temperature" in doc["data"]
        ):
            images = doc["data"]["pe1_image"]
            fig, ax = plt.subplots()
            ax.imshow(images[0], vmax=6000)
            fig.savefig(local_dir.joinpath("dark_subtraction_{}.png".format(count)))
            count += 1
    return
