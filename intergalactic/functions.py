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

def emme(tau, z):
    if tau > 15.13 : return None
    if tau < 3.325e-3 : return 100

    ltau = 9 + math.log10(tau)
    if ltau <= 6.48 : return 100

    ltau = min([ltau, 10.18])

    if z < 0.00025:
        x = -16.1673 + 8.1573 * ltau - 1.51164 * (ltau ** 2) + 0.119703 * (ltau ** 3) - 3.2797e-3 * (ltau ** 4)
    elif 0.00025 <= z < 0.00126:
        x = -18.18504 + 9.132649 * ltau - 1.68782 * (ltau ** 2) + 0.133889 * (ltau ** 3) - 3.71372e-3 * (ltau ** 4)
    elif 0.00126 <= z < 0.0056:
        x = -25.38213 + 12.52873 * ltau - 2.282687 * (ltau ** 2) + 0.1799017 * (ltau ** 3) - 5.049336e-3 * (ltau ** 4)
    elif 0.0056 <= z < 0.0126:
        x = -26.24297 + 12.86747 * ltau - 2.330858 * (ltau ** 2) + 0.1829501 * (ltau ** 3) - 5.130008e-3 * (ltau ** 4)
    elif 0.0126 <= z:
        x = -25.09745 + 12.14146 * ltau - 2.170348 * (ltau ** 2) + 0.1681194 * (ltau ** 3) - 4.645682e-3 * (ltau ** 4)

    emme = 1 / x
    if emme < 0.15 : emme = 0.15
    if emme > 100 : emme = 100

    return emme

def ennea(t):
    if t == 0 : return 0.0
    logt, b = math.log10(t), -1.4
    if logt > b : return 0.003252 * (logt - b)
    return 0.0

def enneb(t):
    if t == 0 : return 0.0
    logt, b = min(math.log10(t), -0.1), -1.2
    if logt > b : return 0.02497 * (logt - b)
    return 0.0

def etout(t):
    if t == 0 : return 0.0
    tc = 5.3e-5
    if t > tc:
        rt = (tc / t) * 0.4
        return 1 - 0.44 * (rt ** 2) * (1 - 0.41 * rt) - 0.22 * (rt **^2)
    else:
        return 8.67e3 * t

