import math

from intergalactic.imfs import Chabrier, Ferrini, Salpeter, Kroupa, MillerScalo, Maschberger, Starburst
from intergalactic.abundances import AndersGrevesse1989, GrevesseSauval1998, Asplund2005, Asplund2009, Heger2010


def select_imf(name, params = {}):
    imfs = {
             "salpeter": Salpeter,
             "chabrier": Chabrier,
             "ferrini": Ferrini,
             "kroupa": Kroupa,
             "miller_scalo": MillerScalo,
             "starburst": Starburst,
             "maschberger": Maschberger
           }
    return imfs[name](params)


def abundances(option, z):
    abundandes_data = {
           "ag89": AndersGrevesse1989,
           "gs98": GrevesseSauval1998,
           "as05": Asplund2005,
           "as09": Asplund2009,
           "he10": Heger2010
          }

    abundances = abundandes_data[option](z)
    solar_abundances = {}
    solar_abundances["x1"] = abundances.x1()
    solar_abundances["x4"] = abundances.x4()
    solar_abundances["feh"] = abundances.feh()
    solar_abundances["data origin"] = abundances.description()

    return solar_abundances

