import math

import intergalactic.imfs as imf
import intergalactic.abundances as ab
import intergalactic.constants as constants

def select_imf(name, params = {}):
    imfs = {
        "salpeter": imf.Salpeter,
        "chabrier": imf.Chabrier,
        "ferrini": imf.Ferrini,
        "kroupa": imf.Kroupa,
        "miller_scalo": imf.MillerScalo,
        "starburst": imf.Starburst,
        "maschberger": imf.Maschberger
    }
    return imfs[name](params)

def select_abundances(option, z):
    abundandes_data = {
        "ag89": ab.AndersGrevesse1989,
        "gs98": ab.GrevesseSauval1998,
        "as05": ab.Asplund2005,
        "as09": ab.Asplund2009,
        "he10": ab.Heger2010
    }
    return abundandes_data[option](z)

def select_dtd(option):
    dtds = {
        "rlp": dtd_ruiz_lapuente,
        "mdvp": dtd_mannucci_della_valle_panagia
    }
    return dtds[option]

def value_in_interval(value, interval = []):
    return min(max(interval[0], value), interval[1])

def secondary_mass_fraction(mu):
    """
    Distribution function of the mass fraction of the secondary in binary systems / SNI
    mu = Mass_secondary / Mass_binary_system
    From: Matteucci, F. & Greggio, L. 1986, A&A, 154, 279
    with Gamma = 2 as Greggio, L., Renzini, A.: 1983a, Astron. Astrophys. 118, 217

    """

    gamma = 2.0
    return (2.0 ** (1.0 + gamma)) * (1.0 + gamma) * (mu ** gamma)

def tau_polinomyal_coefficients(z):
    """
    Coefficients (z-dependent) for the log(tau) formula from
    Raiteri C.M., Villata M. & Navarro J.F., 1996, A&A 315, 105-115

    """
    log_z = math.log10(z)
    log_z_2 = log_z ** 2

    a0 = 10.13 + 0.07547 * log_z - 0.008084 * log_z_2
    a1 = -4.424 - 0.7939 * log_z - 0.1187 * log_z_2
    a2 = 1.262 + 0.3385 * log_z + 0.05417 * log_z_2

    return [a0, a1, a2]

def stellar_lifetime(stellar_m, z):
    """
    Empirical formula for stellar lifetimes from
    Raiteri C.M., Villata M. & Navarro J.F., 1996, A&A 315, 105-115

    """
    log_m = math.log10(stellar_m)
    a0, a1, a2 = tau_polinomyal_coefficients(z)

    log_tau = a0 + a1 * log_m + a2 * (log_m ** 2)

    return math.pow(10, log_tau - 9)

def stellar_mass(tau, z):
    """
    Derived from the stellar lifetimes formula from
    Raiteri C.M., Villata M. & Navarro J.F., 1996, A&A 315, 105-115
    solving the equation for the log(M).
    This function returns always the smaller root, as that is the
    good fit for masses up to the max_mass_allowed(z)

    """
    log_tau = math.log10(tau * 1e9) # years to Gyrs
    a0, a1, a2 = tau_polinomyal_coefficients(z)
    square = math.sqrt((a1 ** 2) - (4 * a2 * (a0 - log_tau)))
    log_mass_minus = (-a1 - square) / (2 * a2)

    return round(math.pow(10, log_mass_minus), 10)

def max_mass_allowed(z):
    """
    The formula for stellar lifetimes from Raiteri et al is a good fit up until
    a (dependent on z) critical mass. After it tau increases and we consider it non valid.

    """
    log_z = math.log10(z)
    log_z_2 = log_z ** 2
    _, a1, a2 = tau_polinomyal_coefficients(z)
    return float(math.floor((math.pow(10, -a1/(2 * a2)))))

def total_energy_ejected(t):
    if t <= 0 : return 0.0
    tc = 5.3e-5
    if t > tc:
        rt = (tc / t) ** 0.4
        return 1 - 0.44 * (rt ** 2) * (1 - 0.41 * rt) - 0.22 * (rt ** 2)
    else:
        return 8.67e3 * t

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

def newton_cotes(a, b, f):
    """
    Integration using Newton-Cotes formula with degree 6 (7 points)
    """
    NEWTON_COTES_POINTS = 7
    NEWTON_COTES_COEFFICIENTS = [0.29285714, 1.54285714, 0.19285714, 1.94285714, 0.19285714, 1.54285714, 0.29285714]

    h = (b - a) / (NEWTON_COTES_POINTS - 1)
    sum_fs = 0.0
    for i in range(0, NEWTON_COTES_POINTS):
        sum_fs += NEWTON_COTES_COEFFICIENTS[i] * f(a + (i * h))

    return h * sum_fs

def imf_binary_primary(m, imf, binary_fraction=constants.BIN_FRACTION):
    """
    Initial mass function for primary stars of binary systems
    Integrated between  m' and m'' using Newton-Cotes
    Returns 0 unless m is in (1.5, 16)

    """

    m_inf = max(constants.B_MIN, m)
    m_sup = min(constants.B_MAX, 2 * m)
    if m <= 0 or m_sup <= m_inf : return 0.0

    return newton_cotes(m_inf, m_sup, phi_primary(m, imf, binary_fraction))

def imf_binary_secondary(m, imf, SNI_events = False, binary_fraction=constants.BIN_FRACTION):
    """
    Initial mass function for secondary stars of binary systems
    Optionally ocurring Supernova I events
    Integrated between  m' and m'' using Newton-Cotes
    If SNI_events = False then returns 0 unless m is in (0, 8)

    """

    m_inf = max(constants.B_MIN, 2 * m)
    m_sup = constants.B_MAX
    if SNI_events : b_sup = min(constants.B_MAX, constants.M_SNII + m)
    if m <= 0 or m_sup <= m_inf : return 0.0

    return newton_cotes(m_inf, m_sup, phi_secondary(m, imf, binary_fraction))

def imf_zero(m, imf, binary_fraction=constants.BIN_FRACTION):
    """
    Initial mass function for stars that are single or
    part of binary systems not giving rise to SN I events

    """

    if constants.B_MIN <= m <= constants.B_MAX:
        return imf.for_mass(m) * (1.0 - binary_fraction)
    else:
        return imf.for_mass(m)

def global_imf(m, imf, binary_fraction=constants.BIN_FRACTION):
    """
    global initial mass function from Ferrini et al.*,1992, ApJ, 387, 138

    """
    if m < constants.M_MIN:
        return 0.0
    if constants.M_MIN <= m < 1.5:
        return imf_zero(m, imf, binary_fraction) + imf_binary_secondary(m, imf, binary_fraction)
    elif 1.5 <= m < 8:
        return imf_zero(m, imf, binary_fraction) + imf_binary_secondary(m, imf, binary_fraction) + imf_binary_primary(m, imf, binary_fraction)
    elif 8 <= m < 16:
        return imf_zero(m, imf, binary_fraction) + imf_binary_primary(m, imf, binary_fraction)
    elif 16 <= m:
        return imf_zero(m, imf, binary_fraction)


def phi_primary(m, imf, binary_fraction=constants.BIN_FRACTION):
    """
    Expression to integrate for each mass m for the IMF for primary stars of binary systems

    """
    return lambda binary_mass : secondary_mass_fraction(1.0 - (m / binary_mass)) * \
                                imf.for_mass(binary_mass) * binary_fraction * \
                                m / (binary_mass ** 2)

def phi_secondary(m, imf, binary_fraction=constants.BIN_FRACTION):
    """
    Expression to integrate for each mass m for the IMF for secondary stars of binary systems

    """
    return lambda binary_mass : secondary_mass_fraction(m / binary_mass) * \
                                imf.for_mass(binary_mass) * binary_fraction * \
                                m / (binary_mass ** 2)
