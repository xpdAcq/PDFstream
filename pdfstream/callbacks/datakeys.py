import typing as T
from functools import lru_cache


class DataKeys:

    def __init__(self, detector: str, image: str) -> None:
        self.image = image
        self.detector = detector
        self.mask = detector + "_mask"
        self.chi_2theta = detector + "_chi_2theta"
        self.chi_Q = detector + "_chi_Q"
        self.chi_I = detector + "_chi_I"
        self.iq_Q = detector + "_iq_Q"
        self.iq_I = detector + "_iq_I"
        self.sq_Q = detector + "_sq_Q"
        self.sq_S = detector + "_sq_S"
        self.fq_Q = detector + "_fq_Q"
        self.fq_F = detector + "_fq_F"
        self.gr_r = detector + "_gr_r"
        self.gr_G = detector + "_gr_G"
        self.gr_argmax = detector + "_gr_argmax"
        self.gr_max = detector + "_gr_max"
        self.chi_argmax = detector + "_chi_argmax"
        self.chi_max = detector + "_chi_max"

    @lru_cache(1)
    def get_2d_arrays(self) -> T.List[str]:
        return [
            self.image,
            self.mask
        ]

    @lru_cache(1)
    def get_1d_arrays(self) -> T.List[str]:
        return [
            self.chi_2theta,
            self.chi_Q,
            self.chi_I,
            self.iq_Q,
            self.iq_I,
            self.sq_Q,
            self.sq_S,
            self.fq_Q,
            self.fq_F,
            self.gr_r,
            self.gr_G
        ]

    @lru_cache(1)
    def get_scalar(self) -> T.List[str]:
        return [
            self.chi_argmax,
            self.chi_max,
            self.gr_argmax,
            self.gr_max
        ]

    @lru_cache(1)
    def get_all(self) -> T.List[str]:
        return self.get_2d_arrays() + \
            self.get_1d_arrays() + \
            self.get_scalar()

    @lru_cache(1)
    def get_pdfgetx_x(self) -> T.List[str]:
        return [self.iq_Q, self.sq_Q, self.fq_Q, self.gr_r]

    @lru_cache(1)
    def get_pdfgetx_y(self) -> T.List[str]:
        return [self.iq_I, self.sq_S, self.fq_F, self.gr_G]
