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
        "greggio-CDD04": dtd_close_dd_04,
        "greggio-CDD1": dtd_close_dd_1,
        "greggio-WDD04": dtd_wide_dd_04,
        "greggio-WDD1": dtd_wide_dd_1,
        "greggio-SDCH": dtd_sd_chandra,
        "greggio-SDSCH": dtd_sd_subchandra,
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
    if t <= 0:
        return 0.0

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


def dtd_close_dd_04(t):
    """
    Delay Time Distribution (DTD) from Laura Greggio, A&A 441, 1055–1078 (2005)
    Model Close Double Degenerate 0.4 Gyrs

    """
    if t <= 0:
        return 0.0

    logt = math.log10(t) + 9
    if logt < 7.657:
        log_dtd = -20
    elif 7.657 <= logt < 8.6:
        log_dtd = -0.8373*(logt**2) + 13.217*logt - 51.878
    else:
        log_dtd = 10.914 - 1.29964*logt

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 2.335e-3


def dtd_close_dd_1(t):
    """
    Delay Time Distribution (DTD) from Laura Greggio, A&A 441, 1055–1078 (2005)
    Model Close Double Degenerate 1 Gyr

    """
    if t <= 0:
        return 0.0

    logt = math.log10(t) + 9

    if logt < 6.32:
        log_dtd = -20
    elif 6.32 <= logt < 7.9:
        log_dtd = 4.68e-3 + 4.86e-2*(logt-6.32)
    elif 7.9 <= logt < 8.987:
        log_dtd = 4.117 - 0.5092*logt
    elif 8.987 <= logt < 9.15:
        log_dtd = -97.154*(logt**3) + 2653.4456*(logt**2) - 24157.978*logt + 73317.501
    else:
        log_dtd = 8.8761 - 1.0656*logt

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 6.423e-4


def dtd_wide_dd_04(t):
    """
    Delay Time Distribution (DTD) from Laura Greggio, A&A 441, 1055–1078 (2005)
    Model Wide Double Degenerate 0.4 Gyrs

    """
    if t <= 0:
        return 0.0

    logt = math.log10(t) + 9
    if logt < 7.5:
        log_dtd = -20
    elif 7.5 <= logt < 8.746:
        log_dtd = -1.1944*(logt**4) + 37.543*(logt**3) - 442.49*(logt**2) + 2318*logt - 4555.6
    else:
        log_dtd = -0.8223*logt + 6.6439

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 3.011e-3


def dtd_wide_dd_1(t):
    """
    Delay Time Distribution (DTD) from Laura Greggio, A&A 441, 1055–1078 (2005)
    Model Wide Double Degenerate 1 Gyr

    """
    if t <= 0:
        return 0.0

    logt = math.log10(t) + 9
    if logt < 7.69:
        log_dtd = -20
    elif 7.69 <= logt < 8.99:
        log_dtd = 0.1305*(logt**4) - 4.2953*(logt**3) + 52.6877*(logt**2) - 285.3629*logt + 575.189
    else:
        log_dtd = 1.2853*(logt**4) - 49.722*(logt**3) + 721.22*(logt**2) - 4649.52*logt + 11241.15

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 5.238e-3


def dtd_sd_chandra(t):
    """
    Delay Time Distribution (DTD) from Laura Greggio, A&A 441, 1055–1078 (2005)
    Model Single Degenerate Chandra Mass

    """
    if t <= 0:
        return 0.0

    logt = math.log10(t) + 9

    if logt < 7.89:
        log_dtd = -20
    elif 7.89 <= logt < 9.1:
        log_dtd = -0.0869*(logt**3) + 1.9168*(logt**2) - 14.187*logt + 35.319
    elif 9.1 <= logt < 9.89:
        log_dtd = -1.7291*logt + 15.144
    else:
        log_dtd = -5.1962*logt + 49.362

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 9.796e-4


def dtd_sd_subchandra(t):
    """
    Delay Time Distribution (DTD) from Laura Greggio, A&A 441, 1055–1078 (2005)
    Model Single Degenerate Sub-Chandra Mass

    """
    if t <= 0:
        return 0.0

    logt = math.log10(t) + 9
    if logt < 7.60:
        log_dtd = -20
    elif 7.60 <= logt < 8.58:
        log_dtd = 0.2564*(logt**3) - 6.8315*(logt**2) + 59.975*logt - 173.57
    else:
        log_dtd = -1.7322*logt + 14.841

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 8.139e-4


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
