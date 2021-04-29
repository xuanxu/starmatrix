"""
Delay Time Distributions

Contains some predefined DTDs from different papers/authors:

* Ruiz Lapuente & Canal (2000)
* Maoz & Graur (2017)
* Castrillo et al (2020)
* Greggio, L. (2005)

"""

import math


def select_dtd(option):
    dtds = {
        "rlp": dtd_ruiz_lapuente,
        "maoz": dtd_maoz_graur,
        "castrillo": dtd_castrillo,
        "greggio": dtd_greggio,
        "chen": dtd_chen
    }
    return dtds[option]


def dtd_correction(params):
    """
    When normalizing DTDs to 1 sometimes a correction factor is needed,
    caused by the uncertainty in the value of the integral of the DTD for the whole mass range

    """
    if "dtd_correction_factor" in params:
        return params["dtd_correction_factor"]

    return 1.0


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

    dtd = (f1 + f2 + f3 + f4 + f5) * 1e9

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    rate = 0.2440759  # [SN / Yr / M*]

    return rate * dtd


def dtd_maoz_graur(t):
    """
    Delay Time Distribution (DTD) from Maoz & Graur (2017)

    """
    if t <= 0.05:
        return 0.0

    dtd = math.pow(t, -1.1)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    rate = 1.793e-4  # [SN / Yr / M*]

    return rate * dtd


def dtd_castrillo(t):
    """
    Delay Time Distribution (DTD) from Castrillo et al (2020, in preparation)

    """
    if t <= 0.04:
        return 0.0

    dtd = math.pow(t, -1.2)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    rate = 1.5879e-4  # [SN / Yr / M*]

    return rate * dtd


def dtd_greggio(t):
    """
    Delay Time Distribution (DTD) from Laura Greggio, A&A 441, 1055–1078 (2005)

    """
    logt = math.log10(t) + 9
    if logt < 7.5:
        dtd = 0
    elif 7.5 <= logt < 7.735:
        dtd = (0.00215/(7.776-7.516)) * (logt-7.50)
    elif 7.735 <= logt < 8.55:
        dtd = 0.003335 * math.exp(((-0.5 * (logt-8.22))/0.47) ** 2)
    elif 8.55 <= logt < 8.61:
        dtd = 0.002618 - ((0.002618-0.001129)/(8.6398-8.55)) * (logt-8.55)
    else:
        dtd = math.pow(10, ((-1.0615 * logt) + 6))

    # Normalization
    return dtd * 0.524563739


def dtd_chen(t):
    """
    Delay Time Distribution (DTD) from Chen, Hu and Wang, 2021, ApJ

    """
    if t <= 0.12:
        return 0.0

    dtd = math.pow(t, -1.41)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    rate = 2.072e-4  # [SN / Yr / M*]

    return rate * dtd
