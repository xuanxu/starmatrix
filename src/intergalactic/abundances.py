"""
Chemical Abundances

Contains solar abundances from different papers/authors:

* Anders & Grevesse 1989,
* Grevesse & Sauval 1998,
* Asplund et al. 2005,
* Asplund et al. 2009,
* Heger 2010
* Lodders et al. 2019

and a way to define new abundances subclassing Abundances

"""

import math


def select_abundances(option, z):
    abundandes_data = {
        "ag89": AndersGrevesse1989,
        "gs98": GrevesseSauval1998,
        "as05": Asplund2005,
        "as09": Asplund2009,
        "he10": Heger2010,
        "lo19": Lodders2019
    }
    return abundandes_data[option](z)


class Abundances:
    def __init__(self, z):
        self.z = z

    def description(self):
        return "Base Abundances class"

    def feh(self):
        if self.z == 0:
            return -20
        else:
            return self.feh_z_non_zero()

    def abundance(self):
        return {
            "H":   self.h(),
            "D":   self.elements()["D"],
            "He3": self.elements()["He3"],
            "He4": self.he4(),
            "C":   self.elements()["C"] * (10 ** self.feh()),
            "C13": self.elements()["C13"] * (10 ** self.feh()),
            "N":   self.elements()["N"] * (10 ** self.feh()),
            "O":   self.elements()["O"] * (10 ** self.feh()),
            "Ne":  self.elements()["Ne"] * (10 ** self.feh()),
            "Mg":  self.elements()["Mg"] * (10 ** self.feh()),
            "Si":  self.elements()["Si"] * (10 ** self.feh()),
            "S":   self.elements()["S"] * (10 ** self.feh()),
            "Ca":  self.elements()["Ca"] * (10 ** self.feh()),
            "Fe":  self.elements()["Fe"] * (10 ** self.feh())
        }

    def corrected_abundance_CRI_LIM(self):
        """
        When using the combination of yields from
        Cristallo et al. 2011 (for low mass stars) + Limongi & Chieffi 2012 (for massive stars)
        data needs to be corrected because for non solar metalicities they don't follow solar scale.
        """
        if self.z < 0.014:
            return {
                "H":   self.h(),
                "D":   self.elements()["D"],
                "He3": self.elements()["He3"],
                "He4": self.he4(),
                "C":   self.elements()["C"] * (10 ** self.feh()),
                "C13": self.elements()["C13"] * (10 ** self.feh()),
                "N":   self.elements()["N"] * (10 ** self.feh()),
                "O":   self.elements()["O"] * (10 ** (self.feh() + 0.47)),
                "Ne":  self.elements()["Ne"] * (10 ** self.feh()),
                "Mg":  self.elements()["Mg"] * (10 ** (self.feh() + 0.27)),
                "Si":  self.elements()["Si"] * (10 ** (self.feh() + 0.37)),
                "S":   self.elements()["S"] * (10 ** (self.feh() + 0.35)),
                "Ca":  self.elements()["Ca"] * (10 ** (self.feh() + 0.33)),
                "Fe":  self.elements()["Fe"] * (10 ** self.feh())
            }
        else:
            return self.abundance()


class AndersGrevesse1989(Abundances):
    def h(self):
        return -2.398 * self.z + 0.7516

    def he4(self):
        return 1.40 * self.z + 0.2484

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.02)

    def elements(self):
        return {
            "H":   0.705e-0,
            "D":   4.840e-5,
            "He3": 2.900e-5,
            "He4": 2.750e-1,
            "C":   3.000e-3,
            "C13": 2.830e-5,
            "N":   1.100e-3,
            "O":   8.600e-3,
            "Ne":  1.690e-3,
            "Mg":  5.200e-4,
            "Si":  6.500e-4,
            "S":   4.000e-4,
            "Ca":  6.000e-5,
            "Fe":  1.200e-3
        }

    def description(self):
        return "Anders & Grevesse 1989"


class GrevesseSauval1998(Abundances):
    def h(self):
        return -2.33 * self.z + 0.7516

    def he4(self):
        return 1.33 * self.z + 0.2484

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.02)

    def elements(self):
        return {
            "H":   0.733e-0,
            "D":   4.800e-5,
            "He3": 2.900e-5,
            "He4": 2.495e-1,
            "C":   2.890e-3,
            "C13": 2.830e-5,
            "N":   8.480e-4,
            "O":   7.880e-3,
            "Ne":  1.750e-3,
            "Mg":  6.650e-4,
            "Si":  7.240e-4,
            "S":   4.980e-4,
            "Ca":  6.680e-5,
            "Fe":  1.290e-3
        }

    def description(self):
        return "Grevesse & Sauval 1998"


class Asplund2005(Abundances):
    def h(self):
        return -1.092 * self.z + 0.75157

    def he4(self):
        return 0.06 * self.z + 0.2484

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.012)

    def elements(self):
        return {
            "H":   0.739e-0,
            "D":   4.800e-5,
            "He3": 2.900e-5,
            "He4": 2.486e-1,
            "C":   2.180e-3,
            "C13": 2.830e-5,
            "N":   6.240e-4,
            "O":   5.400e-3,
            "Ne":  1.020e-3,
            "Mg":  6.010e-4,
            "Si":  6.700e-4,
            "S":   3.270e-4,
            "Ca":  6.040e-5,
            "Fe":  1.170e-3
        }

    def description(self):
        return "Asplund et al. 2005"


class Asplund2009(Abundances):
    def h(self):
        return -1.06167 * self.z + 0.7524

    def he4(self):
        return 0.067 * self.z + 0.2476

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.0134)

    def elements(self):
        return {
            "H":   0.738e00,
            "D":   1.430e-5,
            "He3": 4.490e-5,
            "He4": 2.485e-1,
            "C":   2.384e-3,
            "C13": 2.830e-5,
            "N":   6.986e-4,
            "O":   5.784e-3,
            "Ne":  1.256e-3,
            "Mg":  7.052e-4,
            "Si":  6.688e-4,
            "S":   3.114e-4,
            "Ca":  6.459e-5,
            "Fe":  1.307e-3
        }

    def description(self):
        return "Asplund et al. 2009"


class Heger2010(Abundances):
    def h(self):
        return -2.6866 * self.z + 0.7513

    def he4(self):
        return 1.687 * self.z + 0.2487

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.015)

    def elements(self):
        return {
            "H":   0.711e0,
            "D":   2.76e-5,
            "He3": 3.41e-5,
            "He4": 2.74e-1,
            "C":   2.46e-3,
            "C13": 2.98e-5,
            "N":   7.96e-4,
            "O":   6.60e-3,
            "Ne":  1.17e-3,
            "Mg":  5.65e-4,
            "Si":  7.55e-4,
            "S":   3.96e-4,
            "Ca":  7.13e-5,
            "Fe":  1.26e-3
        }

    def description(self):
        return "Heger 2010"


class Lodders2019(Abundances):
    def h(self):
        return -2.6866 * self.z + 0.7513

    def he4(self):
        return 1.687 * self.z + 0.2487

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.015)

    def elements(self):
        return {
            "H":   0.7048,
            "D":   2.78e-5,
            "He3": 3.47e-5,
            "He4": 0.2786,
            "C":   3.031e-3,
            "C13": 3.432e-5,
            "N":   8.536e-4,
            "O":   7.428e-3,
            "Ne":  2.271e-3,
            "Mg":  5.437e-4,
            "Si":  7.220e-4,
            "S":   3.719e-4,
            "Ca":  6.209e-5,
            "Fe":  1.255e-3
        }

    def description(self):
        return "Lodders et al. 2019"
