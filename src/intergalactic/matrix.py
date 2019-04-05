import numpy as np
import intergalactic.constants as constants
import intergalactic.functions as functions


sn_elements_list = ["He4", "C12", "O16", "N14", "C13", "Ne", "Mg", "Si", "S", "Ca", "Fe"]

"""
Datasets of Supernova ejections for different metallicities:
There's a dataset for lower metallicities (Z=0.004, Z=0.0004)
and another one for higher metalicity values (Z=0.008, Z=0.02 and Z= 0.0317).
In both cases there's data for SN of Ia and Ib types.

Supernova Ia data source: Iwamoto, K. et al. 1999 ApJ 125, 439
Supernova Ib data source: Ferrini, F., Poggianti, B. 1993 ApJ 410, 44

"""

sn_ejections_low_z = {
    "sn_ia": dict(zip(sn_elements_list, [0.0, 0.0508, 0.133, 3.31e-8, 1.56e-9, 0.00229, 0.0158, 0.142, 0.0914, 0.0181, 0.68])),
    "sn_ib": dict(zip(sn_elements_list, [1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3]))
}

sn_ejections_high_z = {
    "sn_ia": dict(zip(sn_elements_list, [0.0, 0.0483, 0.143, 1.16e-6, 1.40e-6, 0.00202, 0.0085, 0.154, 0.0846, 0.0119, 0.626])),
    "sn_ib": dict(zip(sn_elements_list, [1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3]))
}

def empty_q_matrix():
    return np.zeros((15, 15))

def q_index(element):
    q_elements = ["H", "D", "He3", "He4", "C12", "O16", "N14", "C13", "nr", "Ne", "Mg", "Si", "S", "Ca", "Fe"]
    return q_elements.index(element)

def q(m, settings = {}):
    """
    Compute the Q Matrix of elements for a given mass (without supernovas)

    The element production matrix has this structure:
        H  D  He3  He4  C12  O16  N14  C13  nr  Ne  Mg  Si  S  Ca  Fe
    H
    D
    He3
    He4
    C12
    O16
    N14
    C13
    nr
    Ne
    Mg
    Si
    S
    Ca
    Fe

    So element Q(1,1) (internally q(0,0) as numpy index starts at 0) is the H produced from H,
    and Q(14,4) is the Calcium created from Helium 4.
    Returned matrix is cropped to [constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS]

    """

    q = empty_q_matrix()
    if m < constants.M_MIN : return resize_matrix(q)

    z          = settings["z"]
    abundances = settings["abundances"].abundance()
    expelled   = settings["expelled"]
    elements = expelled.for_mass(m)

    h_he = abundances["H"] + abundances["He4"]
    remnant = elements["remnants"]
    he_core = 1 - (elements["H"] / abundances["H"])
    co_core = ((he_core * abundances["H"]) + abundances["He4"] - elements["He4"]) / h_he
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
            ((1 - co_core) * abundances["N"] / (abundances["C"] + abundances["C13"] + abundances["O"])) +
            co_core
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
        fractional_abundances[key] = functions.value_in_interval(value, [0.0, 1.0])

    total_abundances = sum(fractional_abundances.values())
    if total_abundances > 1:
        for key, value in fractional_abundances.items():
            fractional_abundances[key] = value / total_abundances

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
    if constants.M_MIN <= m < 2:
        w3 = (-3.47e-4 * m) + 7.79e-4
    elif 2 <= m <= 3:
        w3 = (-4.43e-5 * m) + 1.74e-4
    elif 3 <= m <= 5:
        w3 = (-1.15e-5 * m) + 7.53e-5
    else:
        w3 = 0.

    fractional_abundances["He3"] = w3 * (1 - remnant) / abundances["H"]

    # Q(i,j) values:
    q[0, 0] = 1 - he_core - fractional_abundances["He3"]
    q[0, 1] = -0.5 * (1 - remnant)
    q[2, 0] = fractional_abundances["He3"]
    q[2, 1] = 1.5 * (1 - he3_core)
    q[2, 2] = 1 - he3_core
    q[3, 0] = he_core - co_core
    q[3, 1] = 1.5 * (he3_core - co_core)
    q[3, 2] = he3_core - co_core
    q[3, 3] = 1 - co_core

    q[4, 0] = fractional_abundances["C"] * new_metals_ejected
    q[5, 0] = fractional_abundances["O"] * new_metals_ejected
    q[6, 0] = fractional_abundances["N"] * new_metals_ejected
    q[7, 0] = fractional_abundances["C13"] * new_metals_ejected

    q[9, 0]  = fractional_abundances["Ne"] * new_metals_ejected
    q[10, 0] = fractional_abundances["Mg"] * new_metals_ejected
    q[11, 0] = fractional_abundances["Si"] * new_metals_ejected
    q[12, 0] = fractional_abundances["S"] * new_metals_ejected
    q[13, 0] = fractional_abundances["Ca"] * new_metals_ejected
    q[14, 0] = fractional_abundances["Fe"] * new_metals_ejected

    # C12  O16  N14  C13  Ne  Mg  Si  S  Ca  Fe
    for i in [4, 5, 6, 7, 9, 10, 11, 12, 13, 14]:
        q[i, 1] = 1.5 * q[i, 0]
        q[i, 2] = q[i, 0]
        q[i, 3] = q[i, 0]

    # n.r.:
    q[8][4] = new_metals_ejected
    q[8][5] = new_metals_ejected
    q[8][6] = new_metals_ejected
    q[8][7] = new_metals_ejected

    # Diagonal
    for i in range(8, 15):
        q[i][i] = 1 - remnant

    # C-N-O cycle:
    q[4, 4] = 1 - secondary_c13_core
    q[5, 5] = 1 - secondary_n_core
    q[6, 6] = 1 - co_core
    q[7, 7] = 1 - secondary_n_core
    q[6, 4] = secondary_n_core - co_core
    q[6, 5] = secondary_n_core - co_core
    q[6, 7] = secondary_n_core - co_core
    q[7, 4] = secondary_c13_core - secondary_n_core

    # No negative values allowed except for H-D (q(0,1)):
    for i in range(0, 15):
        for j in range(0, 15):
            if q[i, j] <= 0.0 and (i != 0 and j != 1) : q[i, j] = 0.0

    return resize_matrix(q)

def q_sn(m, feh=0.0, sn_type="sn_ia"):
    """
    Compute the Q Matrix of elements coming from Supernova events
    Supernovae type can be specified as one of: [sn_ia, sn_ib]

    Returned matrix is cropped to [constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS]

    """

    q = empty_q_matrix()
    if m < constants.M_MIN : return resize_matrix(q)

    if feh < -0.3:
        sn_ejections = sn_ejections_low_z[sn_type]
    else:
        sn_ejections = sn_ejections_high_z[sn_type]

    den = 0.99 * m
    ejected = dict(zip(sn_elements_list, [0.0 for i in range(11)]))
    for element in sn_elements_list:
        ejected[element] = sn_ejections[element] / den
        for i in range(0, 4):
            q[q_index(element), i] = ejected[element]

    # Remnants = Stellar mass - Ejected mass
    remnant = (m - sum(ejected.values())) / m
    remnant = functions.value_in_interval(remnant, [0.0, 1.0])

    # Diagonal for [nr  Ne  Mg  Si  S  Ca  Fe]
    for i in range(8, 15):
        q[i, i] = 1.0 - remnant

    return resize_matrix(q)

def resize_matrix(complete_matrix):
    return complete_matrix[0:constants.Q_MATRIX_ROWS, 0:constants.Q_MATRIX_COLUMNS]
