class DataKeys:

    def __init__(self, image_key: str) -> None:
        detector = image_key.split('_')[0]
        self.image = image_key
        self.detector = detector
        self.mask = detector + "_mask"
        self.chi_2theta = detector + "_chi_2theta"
        self.chi_Q = detector + "_chi_Q"
        self.chi_I = detector + "_chi_I"
        self.iq_Q = detector + "_iq_Q"
        self.iq_I = detector + "_iq_I"
        self.sq_Q = detector + "_sq_Q"
        self.sq_I = detector + "_sq_I"
        self.fq_Q = detector + "_fq_Q"
        self.fq_I = detector + "_fq_I"
        self.gr_r = detector + "_gr_r"
        self.gr_G = detector + "_gr_G"
        self.gr_argmax = detector + "_gr_argmax"
        self.gr_max = detector + "_gr_max"
        self.chi_argmax = detector + "_chi_argmax"
        self.chi_max = detector + "_chi_max"
