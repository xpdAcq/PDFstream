import typing as tp
from bluesky.callbacks.best_effort import BestEffortCallback
from bluesky.callbacks.broker import LiveImage
from configparser import ConfigParser
from event_model import RunRouter

from pdfstream.pipeline.callbacks import LiveMaskedImage, LiveWaterfall
from pdfstream.units import LABELS


class VisConfig(ConfigParser):
    """The configuration of visualization."""

    @property
    def vis_best_effort(self):
        section = self["VIS BEST EFFORT"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {}

    @property
    def vis_masked_image(self):
        section = self["VIS MASKED IMAGE"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "cmap": section.get("cmap")
        }

    @property
    def vis_dk_sub_image(self):
        section = self["VIS DK SUB IMAGE"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {"cmap": section.get("cmap", fallback="viridis")}

    @property
    def vis_chi(self):
        section = self["VIS CHI"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.chi[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.chi[1])
        }

    @property
    def vis_iq(self):
        section = self["VIS IQ"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.iq[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.iq[1])
        }

    @property
    def vis_sq(self):
        section = self["VIS SQ"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.sq[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.sq[1])
        }

    @property
    def vis_fq(self):
        section = self["VIS FQ"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.fq[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.fq[1])
        }

    @property
    def vis_gr(self):
        section = self["VIS GR"]
        if not section.getboolean("enable", fallback=True):
            return None
        return {
            "xlabel": section.get("xlabel", fallback=LABELS.gr[0]),
            "ylabel": section.get("ylabel", fallback=LABELS.gr[1])
        }


class Visualizer(RunRouter):
    """Visualize the analyzed data. It can be subscribed to a live dispatcher."""

    def __init__(self, config: VisConfig):
        factory = VisFactory(config)
        super(Visualizer, self).__init__([factory])


class VisFactory:
    """The factory of visualization callbacks."""

    def __init__(self, config: VisConfig):
        self.config = config
        self.cb_lst = []
        if self.config.vis_best_effort is not None:
            cb = BestEffortCallback()
            cb.disable_table()
            cb.disable_baseline()
            cb.disable_heading()
            self.cb_lst.append(cb)
        if self.config.vis_dk_sub_image is not None:
            self.cb_lst.append(
                LiveImage("dk_sub_image", **self.config.vis_dk_sub_image)
            )
        if self.config.vis_masked_image is not None:
            self.cb_lst.append(
                LiveMaskedImage("dk_sub_image", "mask", **self.config.vis_masked_image)
            )
        for xfield, yfield, vis_config in [
            ("chi_Q", "chi_I", self.config.vis_chi),
            ("iq_Q", "iq_I", self.config.vis_iq),
            ("sq_Q", "sq_S", self.config.vis_sq),
            ("fq_Q", "fq_F", self.config.vis_fq),
            ("gr_r", "gr_G", self.config.vis_gr)
        ]:
            if vis_config is not None:
                self.cb_lst.append(
                    LiveWaterfall(xfield, yfield, **vis_config)
                )

    def __call__(self, name: str, doc: dict) -> tp.Tuple[list, list]:
        if name != "start":
            return [], []
        return self.cb_lst, []


