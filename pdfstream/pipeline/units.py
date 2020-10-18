A = r"$\mathrm{\AA}$"
INV_A = r"$\mathrm{\AA}^{-1}$"
INV_SQ_A = r"$\mathrm{\AA}^{-2}$"
INV_NM = r"$nm^{-1}$"
MM = "mm"
DEG = r"deg"
RAD = r"rad"
ARB = "a. u."

MAP_PYFAI_TO_MPL = {
    "q_nm^-1": INV_NM,
    "q_A^-1": INV_A,
    "2th_deg": DEG,
    "2th_rad": RAD,
    "r_mm": MM
}

MAP_PYFAI_TO_XNAME = {
    "q_nm^-1": "Q",
    "q_A^-1": "Q",
    "2th_deg": "twotheta",
    "2th_rad": "twotheta",
    "r_mm": "r"
}

MAP_PYFAI_TO_YNAME = {
    "q_nm^-1": "I",
    "q_A^-1": "I",
    "2th_deg": "I",
    "2th_rad": "I",
    "r_mm": "I"
}

MAP_PYFAI_TO_DATAFORMAT = {
    "q_nm^-1": "Qnm",
    "q_A^-1": "QA",
    "2th_deg": "twotheta",
    "2th_rad": "twotheta",
}
