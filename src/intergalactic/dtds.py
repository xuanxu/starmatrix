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
        "mdvp": dtd_mannucci_della_valle_panagia
    }
    return dtds[option]

def dtd_ruiz_lapuente(t):
    """
    Delay Time Distribution (DTD) from Ruiz Lapuente

    """
    if t <= 0 : return 0.0
    logt = math.log10(t) + 9
    if logt < 7.8 : return 0.0
    f1 = 0.17e-11  * math.exp(-0.5 * ((logt - 7.744) / 0.08198) ** 2)
    f2 = 0.338e-11 * math.exp(-0.5 * ((logt - 7.9867) / 0.12489) ** 2)
    f3 = 0.115e-11 * math.exp(-0.5 * ((logt - 8.3477) / 0.14675) ** 2)
    f4 = 0.16e-11  * math.exp(-0.5 * ((logt - 9.08) / 0.23) ** 2)
    f5 = 0.02e-11  * math.exp(-0.5 * ((logt - 9.58) / 0.17) ** 2)
    return((f1 + f2 + f3 + f4 + f5) * 1e9)

def dtd_mannucci_della_valle_panagia(t):
    """
    Delay Time Distribution (DTD) from Mannucci, Della Valle, Panagia (2006)

    """
    if t <= 0 : return 0.0
    logt = math.log10(t) + 9
    if logt <= 7.93:
        logDTD = 1.4 - 50.0 * (logt - 7.7)**2
    else:
        logDTD = -0.8 - 0.9 * (logt - 8.7)**2

    return math.exp(logDTD)
