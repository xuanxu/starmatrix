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

    return abundandes_data[option](z)

def tau(emme, z):
    if emme <= 0.15 : emme = 0.15
    x = 1 / emme

    if emme > 100:
        ltau = 6.48
    elif z < 0.00025:
        ltau = 6.4976 + 11.103 * x - 20.424 * (x ** 2) + 18.792 * (x ** 3) - 6.1625 * (x ** 4)
    elif 0.00025 <= z < 0.00126:
        ltau = 6.4899 + 11.327 * x - 21.124 * (x ** 2) + 19.818 * (x ** 3) - 6.649 * (x ** 4)
    elif 0.00126 <= z < 0.0056:
        ltau = 6.4711 + 11.776 * x - 22.155 * (x ** 2) + 21.184 * (x ** 3) - 7.3164 * (x ** 4)
    elif 0.0056 <= z < 0.0126:
        ltau = 6.4572 + 11.889 * x - 22.139 * (x ** 2) + 21.297 * (x ** 3) - 7.4748 * (x ** 4)
    elif 0.0126 <= z:
        ltau = 6.4326 + 11.676 * x - 20.353 * (x ** 2) + 18.775 * (x ** 3) - 6.4300 * (x ** 4)

    if ltau < 6.48:
        ltau = 6.48
    elif ltau > 10.18:
        ltau = 10.18

    return (10 ** ltau) / 1.e9

