"""The analysis server. Process raw image to PDF."""
from bluesky.callbacks.zmq import RemoteDispatcher
from pkg_resources import resource_filename

from pdfstream.pipeline.core import XPDConfig
from pdfstream.pipeline.core import XPDRouter
from .tools import ServerConfig, run_server

CFG = {
    "XPD": resource_filename("pdfstream", "configs/pdf_xpdserver.ini"),
    "PDF": resource_filename("pdfstream", "configs/xpd_xpdserver.ini")
}


class XPDServerConfig(XPDConfig, ServerConfig):
    """The configuration for xpd server."""
    pass


def make_and_run(cfg: str, *, test_tiff_base: str = None):
    """Run the xpd data reduction server."""
    cfg_file = CFG.get(cfg, cfg)
    config = XPDServerConfig()
    config.read(cfg_file)
    if test_tiff_base:
        config.tiff_base = test_tiff_base
    callback = XPDRouter(config)
    dispatcher = RemoteDispatcher(config.address, prefix=config.prefix)
    dispatcher.subscribe(callback)
    run_server(dispatcher)
