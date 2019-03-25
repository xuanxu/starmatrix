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
import intergalactic

class IMF:
    def __init__(self, params = {}):
        self.params = params
        self.set_params()

    def for_mass(self, m):
        self.m = m
        if m <= 0 : return 0.0
        return self.imf()

    def logm(self):
        return math.log10(self.m)

    def set_params(self):
        pass

    def imf(self):
        pass

    def description(self):
        return "Base Initial Mass Function class"


class Salpeter(IMF):
    def imf(self):
        return self.m * 0.20080261 * (self.m ** -(self.alpha()))

    def alpha(self):
        if "imf_alpha" in self.params:
            return self.params["imf_alpha"]
        else:
            return intergalactic.settings.default["imf_alpha"]

    def description(self):
        return "IMF from Salpeter 1955"


class Starburst(IMF):
    def imf(self):
        return self.m * (self.m**-2.35)/2.28707

    def description(self):
        return "IMF from Starburst 1999"


class MillerScalo(IMF):
    def imf(self):
        return 0.0189 * (106 / 2.30) * math.exp(-((self.logm() + 1.02) ** 2) / (2 * (0.68 ** 2)))

    def description(self):
        return "IMF from Miller & Scalo 1979"


class Ferrini(IMF):
    def imf(self):
        return 2.19 * 10 ** (-math.sqrt(0.73 + self.logm() * (1.92 + self.logm() * 2.07))) / self.m ** 0.52

    def description(self):
        return "IMF Ferrini, Palla & Penco 1998"


class Kroupa(IMF):
    def imf(self):
        if self.m >= 0.01 and self.m < 0.08:
            return self.m * 7.945 * (self.m ** -0.3)
        elif self.m >= 0.08 and self.m < 0.5:
            return self.m * 7.945 * 0.08 * (self.m ** -1.3)
        elif self.m >= 0.5 and self.m < 1.0:
            return self.m * 7.945 * 0.04 * (self.m ** -2.3)
        elif self.m >= 1:
            return self.m * 7.945 * 0.04 * (self.m ** -2.7)

    def description(self):
        return "IMF from Kroupa 2002"


class Chabrier(IMF):
    def imf(self):
        if self.m <= 1:
          return 13.78*(0.158/2.3)*math.exp(-((self.logm() - math.log10(0.079))**2)/(2*(0.69**2)))
        elif self.m > 1:
          return 13.78*self.m*(0.0443/2.3)*(self.m**-2.35)

    def description(self):
        return "IMF from Chabrier 2003"


class Maschberger(IMF):
    def imf(self):
        return self.factor() * self.m * self.a() * \
               (self.m_mu() ** (-self.aalfa())) * \
               ((1 + (self.m_mu() ** (1 - self.aalfa()))) ** (-self.beta()))

    def factor(self):
        if self.params["m_max"] <= 40:
            return 1.31
        else:
            return 1.22

    def m_mu(self):
        return self.m / self.mu()

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

    def set_params(self):
        if "m_max" not in self.params:
            self.params["m_max"] = 40

    def description(self):
        return "IMF from Maschberger 2012"
