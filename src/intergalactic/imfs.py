"""
Initial Mass Functions

Contains some predefined IMFs from different papers/authors:

* Salpeter 1955
* Miller & Scalo 1979
* Ferrini, Palla & Penco 1998
* Starburst 1999
* Kroupa 2002
* Chabrier 2003
* Maschberger 2012

and a way to define new functions subclassing IMF

"""
import math
import scipy.integrate
import intergalactic.settings


def select_imf(name, params={}):
    imfs = {
        "salpeter": Salpeter,
        "starburst": Starburst,
        "chabrier": Chabrier,
        "ferrini": Ferrini,
        "kroupa": Kroupa,
        "miller_scalo": MillerScalo,
        "maschberger": Maschberger
    }
    return imfs[name](params)


class M_IMF:
    def __init__(self, imf):
        self.imf = imf

    def for_mass(self, m):
        return m * self.imf.for_mass(m)


class IMF:
    def __init__(self, params={}):
        self.params = params
        self.set_mass_limits()
        self.normalization_factor = 1.0 / self.integration_of_mass_interval()
        self.set_params()

    def integration_of_mass_interval(self):
        return scipy.integrate.quad(self.imf, self.m_low, self.m_up)[0]

    def for_mass(self, m):
        if m <= 0:
            return 0.0

        return self.normalization_factor * self.imf(m)

    def set_mass_limits(self):
        if "imf_m_low" in self.params:
            self.m_low = self.params["imf_m_low"]
        else:
            self.m_low = intergalactic.settings.default["imf_m_low"]

        if "imf_m_up" in self.params:
            self.m_up = self.params["imf_m_up"]
        else:
            self.m_up = intergalactic.settings.default["imf_m_up"]

    def set_params(self):
        pass

    def imf(self, m):
        return 1.0

    def description(self):
        return "Base Initial Mass Function class"


class Salpeter(IMF):
    def imf(self, m):
        return (m ** -(self.alpha()))

    def alpha(self):
        if "imf_alpha" in self.params:
            return self.params["imf_alpha"]
        else:
            return intergalactic.settings.default["imf_alpha"]

    def description(self):
        return "IMF from Salpeter 1955"


class Starburst(Salpeter):

    def set_mass_limits(self):
        self.m_low = 1.0
        self.m_up = 120.0

    def description(self):
        return "IMF from Starburst 1999"


class MillerScalo(IMF):
    def imf(self, m):
        return math.exp(-((math.log10(m) + 1.02) ** 2) / (2 * (0.68 ** 2))) / m

    def description(self):
        return "IMF from Miller & Scalo 1979"


class Ferrini(IMF):
    def imf(self, m):
        return 10 ** (-math.sqrt(0.73 + math.log10(m) * (1.92 + math.log10(m) * 2.07))) / m ** 1.52

    def description(self):
        return "IMF Ferrini, Palla & Penco 1998"


class Kroupa(IMF):
    def imf(self, m):
        if 0.015 <= m < 0.08:
            return (m ** -0.35)
        elif 0.08 <= m < 0.5:
            return 0.08 * (m ** -1.3)
        elif 0.5 <= m < 1.0:
            return 0.04 * (m ** -2.3)
        elif 1 <= m:
            return 0.04 * (m ** -2.7)
        else:
            return 0

    def description(self):
        return "IMF from Kroupa 2002"


class Chabrier(IMF):
    def imf(self, m):
        if m <= 1:
            return 0.086*m*math.exp(-((math.log10(m) - math.log10(0.22))**2)/(2*(0.57**2)))
        else:
            return 0.043*(m**-2.35)

    def description(self):
        return "IMF from Chabrier 2003"


class Maschberger(IMF):
    def set_mass_limits(self):
        self.m_low = 0.15
        self.m_up = 100.0

    def imf(self, m):
        return self.a() * \
               (self.m_mu(m) ** (-self.aalfa())) * \
               ((1 + (self.m_mu(m) ** (1 - self.aalfa()))) ** (-self.beta()))

    def m_mu(self, m):
        return m / self.mu()

    def g1(self):
        return (1 + ((0.15 / 0.2) ** (1 - self.aalfa()))) ** (1 - self.beta())

    def g2(self):
        return (1 + ((100 / 0.2) ** (1 - self.aalfa()))) ** (1 - self.beta())

    def a(self):
        return ((1 - self.aalfa()) * (1 - self.beta()) / self.mu()) * (1 / (self.g2() - self.g1()))

    def mu(self):
        return 0.2

    def aalfa(self):
        return 2.3

    def beta(self):
        return 1.4

    def description(self):
        return "IMF from Maschberger 2012"
