import numpy as np
import intergalactic.constants as constants
import intergalactic.functions as functions
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
        "D":   0.0,
        "He3": 0.0,
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

    # Make sure all values are in [0, 1] and normalize:
    for key, value in fractional_abundances.items():
        fractional_abundances[key] = functions.value_in_interval(value, [0, 1])

    total_abundances = sum(fractional_abundances.values())
    if total_abundances > 1:
        for key, value in fractional_abundances.items():
            fractional_abundances[key] = value / total

    # He3 core:
    if m <= 3:
        he3_core = he_core
    elif 3 < m <= 8:
        he3_core = 0.282 + 0.026 * m
    elif 8 < m <= 15:
        he3_core = 0.33 + 0.02 * m
    elif 15 < m <= 25:
        he3_core = 0.525 + 0.007 * m
    elif 25 < m <= 50:
        he3_core = 0.63 + 0.00288 * m
    elif 50 < m:
        he3_core = 0.73 + 0.0008 * m

    # Omega He3:
    if constants.MMIN <= m < 2:
        w3 = -3.47 - (4 * m) + 7.79e-4
    elif 2 <= m <= 3:
        w3 = -4.43 - (5 * m) + 1.74e-4
    elif 3 <= m <= 5:
        w3 = -1.15 - (5 * m) + 7.53e-5
    else:
        w3 = 0

    fractional_abundances["He3"] = w3 * (1 - remnant) / abundances["H"]
