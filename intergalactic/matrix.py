import math
import intergalactic.constants as constants
import intergalactic.settings as settings
import intergalactic.elements as elements


"""
Datasets of Supernova ejections for different metallicities:
There's a dataset for lower metallicities (Z=0.004, Z=0.0004)
and another one for higher metalicity values (Z=0.008, Z=0.02 y Z= 0.0317).
In both cases there's data for SN of Ia and Ib types.

"""
elements_list = ["H", "He4", "C", "O", "N", "Ne", "Mg", "Si", "S", "Ca", "Fe"]

sn_ejections_low_z = {
    "sn_ia": dict(zip(elements_list, [0.0, 0.051, 0.133, 0.0, 0.0, 0.00229, 0.0158, 0.142, 0.0914, 0.0181, 0.68])),
    "sn_ib": dict(zip(elements_list, [1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3]))
}

sn_ejections_high_z = {
    "sn_ia": dict(zip(elements_list, [0.0, 0.0483, 0.143, 0.0, 0.0, 0.00202, 0.0085, 0.154, 0.0846, 0.0119, 0.626])),
    "sn_ib": dict(zip(elements_list, [1.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3]))
}

def q(m, settings):
    """
    Compute the Q Matrix of elements for a given mass

    """
    pass
