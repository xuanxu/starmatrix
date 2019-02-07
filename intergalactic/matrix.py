import numpy as np
import intergalactic.constants as constants
import intergalactic.settings as settings
import intergalactic.elements as elements



elements_list = ["H", "He4", "C", "O", "N", "Ne", "Mg", "Si", "S", "Ca", "Fe"]

"""
Datasets of Supernova ejections for different metallicities:
There's a dataset for lower metallicities (Z=0.004, Z=0.0004)
and another one for higher metalicity values (Z=0.008, Z=0.02 y Z= 0.0317).
In both cases there's data for SN of Ia and Ib types.

"""

sn_ejections_low_z = {
    "sn_ia": dict(zip(elements_list, [0.0, 0.051, 0.133, 0.0, 0.0, 0.00229, 0.0158, 0.142, 0.0914, 0.0181, 0.68])),
    "sn_ib": dict(zip(elements_list, [1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3]))
}

sn_ejections_high_z = {
    "sn_ia": dict(zip(elements_list, [0.0, 0.0483, 0.143, 0.0, 0.0, 0.00202, 0.0085, 0.154, 0.0846, 0.0119, 0.626])),
    "sn_ib": dict(zip(elements_list, [1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3]))
}

def q(m, settings = {}):
    """
    Compute the Q Matrix of elements for a given mass

    """

    q = np.zeros((15, 15))
    if m < constants.MMIN : return q

    z          = settings["z"]
    abundances = settings["abundances"]
    expelled   = settings["expelled"]
    elements = expelled.for_mass(m)

    h_he = abundances["H"] + abundances["He4"]
    remnant = elements["remnants"]
    he_core = 1 - (elements["H"] / abundances["H"])
    co_core = (((he_core * abundances["H"]) + abundances["He4"] - elements["He4"]) / h_he)
    new_metals_ejected = max(co_core - remnant, 0.0)

    fractional_abundances = {
        "N":   0.0,
        "C":   0.0,
        "C13": 0.0,
        "O":   0.0,
        "Ne":  0.0,
        "Mg":  0.0,
        "Si":  0.0,
        "S":   0.0,
        "Ca":  0.0,
        "Fe":  0.0
    }

    # Secondary production of N and C is different for massive starts (< 8 solar masses)
    if m >= 8 and z != 0:
        elements["N14s"] += elements["N14p"]
        elements["C13s"] += elements["C13"]
        elements["N14p"] = 0.0
        elements["C13"]  = 0.0

    if z == 0:
        elements["N14s"] = 0.0
        elements["C13s"] = 0.0
        secondary_n_core = 0.0
        secondary_c13_core = 0.0
    else:
        secondary_n_core = (
            (elements["N14s"] / (abundances["C"] + abundances["C13"] + abundances["O"])) -
            ((1 - co_core) * abundances["N"] / (abundances["C"] + abundances["C13"] + abundances["O"]))
        )
        secondary_c13_core = (
            (elements["C13s"] / abundances["C"]) -
            ((1 - secondary_n_core) * (abundances["C13"] / abundances["C"])) +
            secondary_n_core
        )

    if new_metals_ejected != 0:
        fractional_abundances["N"] = elements["N14p"] / (h_he * new_metals_ejected)
        fractional_abundances["C13"] = elements["C13"] / (h_he * new_metals_ejected)
        fractional_abundances["C"] = (
            (elements["C12"] / (h_he * new_metals_ejected)) -
            ((1 - secondary_c13_core) * abundances["C"] / (h_he * new_metals_ejected))
        )
        fractional_abundances["O"] = (
            (elements["O16"] / (h_he * new_metals_ejected)) -
            ((1 - secondary_n_core) * abundances["O"] / (h_he * new_metals_ejected))
        )
        if m >= 8:
            for element in ["Ne", "Mg", "Si", "S", "Ca", "Fe"]:
                fractional_abundances[element] = (
                    (elements[element] - ((1 - remnant) * abundances[element])) /
                    (h_he * new_metals_ejected)
                )
