import pytest
import numpy as np
import intergalactic.functions as functions
import intergalactic.constants as constants
import intergalactic.settings as settings
from intergalactic.imfs import Chabrier, Ferrini, Salpeter, Kroupa, MillerScalo, Maschberger, Starburst
from intergalactic.abundances import AndersGrevesse1989, GrevesseSauval1998, Asplund2005, Asplund2009, Heger2010

def test_select_imf():
    strings = ["salpeter", "chabrier", "ferrini", "kroupa", "miller_scalo", "starburst", "maschberger"]
    classes = [Salpeter, Chabrier, Ferrini, Kroupa, MillerScalo, Starburst, Maschberger]

    for i in range(len(strings)):
        imf_instance = functions.select_imf(strings[i])
        assert type(imf_instance) == classes[i]

def test_select_abundances():
    strings = ["ag89", "gs98", "as05", "as09", "he10"]
    classes = [AndersGrevesse1989, GrevesseSauval1998, Asplund2005, Asplund2009, Heger2010]

    for i in range(len(strings)):
        abundance_instance = functions.select_abundances(strings[i], 0.033)
        assert type(abundance_instance) == classes[i]
        assert abundance_instance.z == 0.033

def test_select_dtd():
    strings = ["rlp", "mdvp"]
    dtds = [functions.dtd_ruiz_lapuente, functions.dtd_mannucci_della_valle_panagia]

    for i in range(len(strings)):
        for time in np.random.rand(5) * 900 * 0.01:
            assert functions.select_dtd(strings[i])(time) == dtds[i](time)

def test_secondary_mass_fraction():
    for m in [0.33, 3.33, 33.7, 73.0]:
        assert functions.secondary_mass_fraction(m) == 24 * m ** 2

def test_mean_lifetime_stellar_mass_relation():
    z                 = 0.02
    stellar_mass_test = 4.0
    lifetime_test     = 0.15

    stellar_mass      = functions.stellar_mass(lifetime_test, z)
    lifetime          = functions.stellar_lifetime(stellar_mass_test, z)

    assert np.isclose(functions.stellar_mass(lifetime, z), stellar_mass_test,  rtol = 0.005)
    assert np.isclose(functions.stellar_lifetime(stellar_mass, z), lifetime_test, rtol = 0.005)

def test_value_in_interval():
    interval_min  = 1.0
    interval_max  = 100
    interval      = [interval_min, interval_max]
    value_in      = 25
    value_out_min = 0.8
    value_out_max = 101

    assert functions.value_in_interval(value_in, interval) == value_in
    assert functions.value_in_interval(value_out_min, interval) == interval_min
    assert functions.value_in_interval(value_out_max, interval) == interval_max

def test_no_negative_time_values():
    t = -1
    assert functions.total_energy_ejected(t) == 0.0
    assert functions.dtd_ruiz_lapuente(t) == 0.0
    assert functions.dtd_mannucci_della_valle_panagia(t) == 0.0

def test_imf_zero():
    m_in_binaries_range = 5.0
    m = constants.B_MIN - 0.5
    imf = functions.select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)

    assert functions.imf_zero(m, imf) == imf.for_mass(m)

    imf_bin = imf.for_mass(m_in_binaries_range) * (1.0 - constants.BIN_FRACTION)
    assert functions.imf_zero(m_in_binaries_range, imf) == imf_bin
