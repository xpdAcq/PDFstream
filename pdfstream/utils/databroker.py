"""Helpers for databrokers."""
import typing as tp

import xarray as xr
from databroker import Broker
from databroker.core import BlueskyRunFromGenerator


# TODO: test function
def query_dark(dark_id: str, stream_name: str, det_name: str, db: Broker) -> tp.Union[xr.DataArray, None]:
    try:
        run = db[dark_id]
    except KeyError:
        return None
    primary: BlueskyRunFromGenerator = getattr(run, stream_name)
    dark_img: xr.DataArray = primary.read()[det_name]
    dark_img = dark_img.squeeze(drop=True)
    return dark_img
