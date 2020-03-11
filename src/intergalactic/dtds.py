"""
Delay Time Distributions

Contains some predefined DTDs from different papers/authors:

* Ruiz Lapuente
* Mannucci, Della Valle, Panagia (2006)

"""

import math


def select_dtd(option):
    dtds = {
        "rlp": dtd_ruiz_lapuente,
        "mdvp": dtd_mannucci_della_valle_panagia,
        "maoz": dtd_maoz_graur,
        "castrillo": dtd_castrillo
    }
    return dtds[option]


def dtd_ruiz_lapuente(t):
    """
    Delay Time Distribution (DTD) from Ruiz Lapuente & Canal (2000)

    """
    if t <= 0:
        return 0.0

    logt = math.log10(t) + 9
    if logt < 7.8:
        return 0.0

    f1 = 0.170e-11 * math.exp(-0.5 * ((logt - 7.744) / 0.08198) ** 2)
    f2 = 0.338e-11 * math.exp(-0.5 * ((logt - 7.9867) / 0.12489) ** 2)
    f3 = 0.115e-11 * math.exp(-0.5 * ((logt - 8.3477) / 0.14675) ** 2)
    f4 = 0.160e-11 * math.exp(-0.5 * ((logt - 9.08) / 0.23) ** 2)
    f5 = 0.020e-11 * math.exp(-0.5 * ((logt - 9.58) / 0.17) ** 2)
    return((f1 + f2 + f3 + f4 + f5) * 1e9)


def dtd_mannucci_della_valle_panagia(t):
    """
    Delay Time Distribution (DTD) from Mannucci, Della Valle, Panagia (2006)

    """
    if t <= 0:
        return 0.0

    logt = math.log10(t) + 9
    if logt <= 7.93:
        logDTD = 1.4 - 50.0 * (logt - 7.7)**2
    else:
        logDTD = -0.8 - 0.9 * (logt - 8.7)**2

    return math.pow(10, logDTD)


def dtd_maoz_graur(t):
    """
    Delay Time Distribution (DTD) from Maoz & Graur (2017)

    """
    if t <= 0.05 or t > 10.0:
        return 0.0

    dtd = math.pow(t, -1.1)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    rate = 0.727  # [SN / Yr / M*]

    return rate * dtd


def dtd_castrillo(t):
    """
    Delay Time Distribution (DTD) from Castrillo et al (2020, in preparation)

    """
    if t <= 0.04:
        return 0.0

    dtd = math.pow(t, -1.2)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    rate = 0.012556  # [SN / Yr / M*]

    return rate * dtd
