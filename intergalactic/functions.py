import math

from intergalactic.imfs import Chabrier, Ferrini, Salpeter, Kroupa, MillerScalo, Maschberger, Starburst


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


def imf():
    if option == 1979:
        return "miller_scalo"
    elif option == 1998:
        return "ferrini"
    elif option == 1999:
        return "starburst"
    elif option == 2002:
        return "kroupa"
    elif option == 2003:
        return "chabrier"
    elif option == 2012:
        return "maschberger"
    elif option < 1000:
        return "salpeter"
