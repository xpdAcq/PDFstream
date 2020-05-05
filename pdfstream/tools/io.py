"""The input / output functions related to file system."""
from pathlib import Path

import fabio
import pyFAI
from diffpy.pdfgetx import PDFConfig, PDFGetter


def load_ai_from_poni_file(poni_file: str):
    """Initiate the AzimuthalIntegrator using poni file."""
    ai = pyFAI.load(poni_file)
    return ai


def load_ai_from_calib_result(calib_result: dict):
    """Initiate the AzimuthalIntegrator using calibration information."""
    ai = pyFAI.AzimuthalIntegrator()
    ai.set_config(calib_result)
    return ai


def load_img(img_file: str):
    """Load the img data from the img_file."""
    img = fabio.open(img_file).data
    return img


def load_pdfconfig(cfg_file: str):
    """Load the PDFConfig from the processed data file or configuration file."""
    pdfconfig = PDFConfig()
    pdfconfig.readConfig(cfg_file)
    return pdfconfig


def write_out(saving_dir: str, filename: str, pdfgetter: PDFGetter):
    """Write out data in pdfgetter into files"""
    data_dirs = {}
    for out_type in pdfgetter.config.outputtypes:
        data_dir = Path(saving_dir).joinpath(out_type)
        if not data_dir.exists():
            data_dir.mkdir()
        data_dirs.update({out_type: data_dir})
    dct = {}
    for out_type in pdfgetter.config.outputtypes:  # out_type in ('iq', 'sq', 'fq', 'gr')
        data_dir = data_dirs.get(out_type)
        out_file = data_dir.joinpath(Path(filename).with_suffix(".{}".format(out_type)).name)
        pdfgetter.writeOutput(str(out_file), out_type)
        dct.update({out_type: str(out_file)})
    return dct
