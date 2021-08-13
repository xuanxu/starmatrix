"""
Delay Time Distributions

Contains some predefined DTDs from different papers/authors:

* Ruiz Lapuente & Canal (2000)
* Maoz & Graur (2017)
* Castrillo et al (2020)
* Greggio, L. (2005)
* Strolger et al. (2020)

"""

import math
import scipy.integrate
import starmatrix.constants as constants
from functools import lru_cache


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
        "chen": dtd_chen,
        "strolger-fit1": dtds_strolger["fit_1"],
        "strolger-fit2": dtds_strolger["fit_2"],
        "strolger-fit3": dtds_strolger["fit_3"],
        "strolger-fit4": dtds_strolger["fit_4"],
        "strolger-fit5": dtds_strolger["fit_5"],
        "strolger-optimized": dtds_strolger["optimized"],
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
    if logt < 7.45:
        dtd = 0
    elif 7.45 <= logt <= 7.735:
        dtd = (0.00215/(7.776-7.516)) * (logt-7.50)
    elif 7.735 < logt <= 8.55:
        dtd = 0.003335 * math.exp(((-0.5 * (logt-8.22))/0.47) ** 2)
    elif 8.55 < logt <= 8.61:
        dtd = 0.002618 - ((0.002618-0.001129)/(8.6398-8.55)) * (logt-8.55)
    elif 8.61 < logt:
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
    elif 8.6 <= logt:
        log_dtd = 10.914 - 1.2964*logt

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 1.059e-3


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
    elif 8.987 <= logt < 9.16:
        log_dtd = -97.15408482273*(logt**3) + 2653.445666247*(logt**2) - 24157.97809549*logt + 73317.50108578
    elif 9.16 <= logt:
        log_dtd = 8.8761 - 1.0656*logt

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 9.8400244741154628e-4


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
        log_dtd = -1.194384*(logt**4) + 37.542520*(logt**3) - 442.490023*(logt**2) + 2318.164371*logt - 4555.628418
    elif 8.746 <= logt:
        log_dtd = -0.81857*logt + 6.60771

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 9.92573144e-4


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
        log_dtd = 0.130499*(logt**4) - 4.295277*(logt**3) + 52.687732*(logt**2) - 285.362875*logt + 575.188754
    elif 8.99 <= logt:
        log_dtd = 1.061260*(logt**4) - 41.103454*(logt**3) + 596.908266*(logt**2) - 3852.941647*logt + 9327.789697

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 1.1169615977359982e-3


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
    elif 9.89 <= logt:
        log_dtd = -5.1962*logt + 49.362

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 1.064741165931863e-3


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
    elif 8.58 <= logt:
        log_dtd = -1.733*logt + 14.852

    dtd = math.pow(10, log_dtd)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    return dtd * 1.0354065248871394e-3


def dtd_chen(t):
    """
    Delay Time Distribution (DTD) from Chen, Hu and Wang, 2021, ApJ

    """
    if t <= 0.12:
        return 0.0

    dtd = math.pow(t, -1.41)

    # Normalization using 1.03e-3 SN/M* as Hubble-time-integrated production efficiency SN/Mo
    rate = 2.069e-4  # [SN / Yr / M*]

    return rate * dtd


class Strolger:
    def __init__(self, psi, omega, alpha):
        self.psi = psi
        self.omega = omega
        self.alpha = alpha

    def description(self):
        return ("Delay Time Distributions (DTDs) from Strolger et al, "
                "The Astrophysical Journal, 2020, 890, 2. "
                "DOI: 10.3847/1538-4357/ab6a97")

    def phi(self, t_gyrs):
        t_myrs = t_gyrs * 1e3

        u = t_myrs - self.psi
        term_1 = (1/(self.omega * math.pi)) * math.exp((-(u**2))/(2*(self.omega**2)))

        t_low = -math.inf
        t_up = self.alpha*(u/self.omega)

        if 12 < t_up:
            term_2 = 2 * scipy.integrate.quad(self.term_2_f, t_low, 0)[0]
        else:
            term_2 = scipy.integrate.quad(self.term_2_f, t_low, t_up)[0]

        return term_1 * term_2

    def term_2_f(self, t_prime):
        return math.exp(-math.pow(t_prime, 2)/2)

    @lru_cache(maxsize=128)
    def normalization_rate(self):
        return self.efficiency() / self.phi_integrated()

    def efficiency(self):
        # SN/M* as Hubble-time-integrated production efficiency SN/Mo
        return 1.03e-3

    def phi_integrated(self):
        return scipy.integrate.quad(self.phi, 0, constants.TOTAL_TIME)[0]

    def at_time(self, t):
        return self.normalization_rate() * self.phi(t)


dtds_strolger = {
    "fit_1": Strolger(10, 600, 220).at_time,
    "fit_2": Strolger(110, 1000, 2).at_time,
    "fit_3": Strolger(350, 1200, 20).at_time,
    "fit_4": Strolger(6000, 6000, -2).at_time,
    "fit_5": Strolger(-650, 2200, 1100).at_time,
    "optimized": Strolger(-1518, 51, 50).at_time,
}
