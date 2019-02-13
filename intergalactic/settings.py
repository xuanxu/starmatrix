"""
Default settings and initial parameters

All the values set here can be overwritten via the input file: params.yml

"""

from intergalactic import constants as constants

default = {
    "z": 0.02,
    "sol_ab": "as09",
    "fe_coef": 1,
    "imf": "kroupa",
    "imf_alpha": 2.35,
    "m_max": constants.MMAX,
    "alpha_bin_stars": 0.05,
    "sn_ia_selection": "rlp"
}
