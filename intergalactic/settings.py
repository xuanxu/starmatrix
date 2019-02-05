"""Default settings and initial parameters
All the values set here can be overwritten by the user in the input file: params.json
"""
from intergalactic import constants as constants

default = {
    "z": 0.02,
    "lim_yields": "GAV",
    "massive_yields": "CLI",
    "sol_ab": "ag89",
    "fe_coef": 1,
    "imf": 2.35,
    "imf_m_up": 40.0,
    "alpha_bin_stars": 0.05,
    "sn_ia_selection": 3,
    "m_max": constants.MMAX
}
