"""Initial Mass Functions

Contains solar abundances from different papers/authors:

* Anders & Grevesse 1989,
* Grevesse & Sauval 1998,
* Asplund et al. 2005,
* Asplund et al. 2009,
* Heger 2010

and a way to define new abundances subclassing Abundances
"""
import math

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

class AndersGrevesse1989(Abundances):
    def x1(self):
        return -2.398 * self.z + 0.7516

    def x4(self):
        return 1.40 * self.z + 0.2484

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.02)

    def elements():
        return {   
                    "H":     0.705e-0,
                    "D":     4.840e-5, 
                    "He3":   2.900e-5,   	   
                    "He4":   2.750e-1,
                    "C":     3.000e-3,   
                    "13C":   2.830e-5,
                    "N":     1.100e-3,
                    "O":     8.600e-3,
                    "Ne":    1.690e-3,
                    "Mg":    5.200e-4,
                    "Si":    6.500e-4,
                    "S":     4.000e-4,
                    "Ca":    6.000e-5,
                    "Fe":    1.200e-3
               }
    def description(self):
        return "Anders & Grevesse 1989"


class GrevesseSauval1998(Abundances):
    def x1(self):
        return -2.33 * self.z + 0.7516

    def x4(self):
        return 1.33 * self.z + 0.2484

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.02)

    def description(self):
        return "Grevesse & Sauval 1998"


class Asplund2005(Abundances):
    def x1(self):
        return -1.092 * self.z + 0.75157

    def x4(self):
        return 0.06 * self.z + 0.2484

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.012)

    def description(self):
        return "Asplund et al. 2005"


class Asplund2009(Abundances):
    def x1(self):
        return -1.06167 * self.z + 0.7524

    def x4(self):
        return 0.067 * self.z + 0.2476

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.0134)

    def description(self):
        return "Asplund et al. 2009"


class Heger2010(Abundances):
    def x1(self):
        return -2.6866 * self.z + 0.7513

    def x4(self):
        return 1.687 * self.z + 0.2487

    def feh_z_non_zero(self):
        return math.log10(self.z / 0.015)

    def description(self):
        return "Heger 2010"


"""
    #     A&G89        G&S98         Aspl05      Asp09      heg10     Asp09          
"H":     0.705e-0     0.733e-0     0.739e-0     0.738e00   0.711e0  0.7154e0    	   
"D":     4.840e-5     4.800e-5     4.800e-5     1.430e-5   2.76e-5  1.430e-5   	   
"He3":   2.900e-5     2.900e-5     2.900e-5     4.490e-5   3.41e-5  4.490e-5   	   
"He4":   2.750e-1     2.495e-1     2.486e-1     2.485e-1   2.74e-1  2.703e-1   	   
"C":     3.000e-3     2.890e-3     2.180e-3     2.384e-3   2.46e-3  2.534e-3   	   
"13C":   2.830e-5     2.830e-5     2.830e-5     2.830e-5   2.98e-5  2.830e-5   
"N":     1.100e-3     8.480e-4     6.240e-4     6.986e-4   7.96e-4  7.425e-4   	   
"O":     8.600e-3     7.880e-3     5.400e-3     5.784e-3   6.60e-3  6.147e-3   	   
"Ne":    1.690e-3     1.750e-3     1.020e-3     1.256e-3   1.17e-3  1.335e-3   	   
"Mg":    5.200e-4     6.650e-4     6.010e-4     7.052e-4   5.65e-4  7.495e-4   	   
"Si":    6.500e-4     7.240e-4     6.700e-4     6.688e-4   7.55e-4  7.107e-4   	   
"S":     4.000e-4     4.980e-4     3.270e-4     3.114e-4   3.96e-4  3.309e-4   	       
"Ca":    6.000e-5     6.680e-5     6.040e-5     6.459e-5   7.13e-5  6.865e-5   	      
"Fe":    1.200e-3     1.290e-3     1.170e-3     1.307e-3   1.26e-3  1.389e-3   
"""

