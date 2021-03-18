import pytest
import numpy as np
import starmatrix.functions as functions
import starmatrix.constants as constants
import starmatrix.settings as settings
import starmatrix.elements as elements
from starmatrix.imfs import select_imf


def test_value_in_interval():
    interval_min = 1.0
    interval_max = 100
    interval = [interval_min, interval_max]
    value_in = 25
    value_out_min = 0.8
    value_out_max = 101

    assert functions.value_in_interval(value_in, interval) == value_in
    assert functions.value_in_interval(value_out_min, interval) == interval_min
    assert functions.value_in_interval(value_out_max, interval) == interval_max


def test_secondary_mass_fraction():
    for m in [0.33, 3.33, 33.7, 73.0]:
        assert functions.secondary_mass_fraction(m) == 24 * m ** 2


def test_mean_lifetime_stellar_mass_relation():
    z = 0.02
    stellar_mass_test = 4.0
    lifetime_test = 0.15

    stellar_mass = functions.stellar_mass(lifetime_test, z)
    lifetime = functions.stellar_lifetime(stellar_mass_test, z)

    assert np.isclose(functions.stellar_mass(lifetime, z), stellar_mass_test,  rtol=0.005)
    assert np.isclose(functions.stellar_lifetime(stellar_mass, z), lifetime_test, rtol=0.005)


def test_total_energy_no_negative_time_values():
    t = -1
    assert functions.total_energy_ejected(t) == 0.0

    assert functions.total_energy_ejected(1e-5) > 0.0

    t = functions.stellar_lifetime(5, 0.02)
    assert functions.total_energy_ejected(t) > 0.0


def test_imf_zero():
    m_in_binaries_range = 5.0
    m_lower = constants.B_MIN - 0.5
    m_up = constants.B_MAX + 0.5
    imf = select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)

    assert functions.imf_zero(m_lower, imf) == imf.for_mass(m_lower)
    assert functions.imf_zero(m_up, imf) == imf.for_mass(m_up)

    imf_bin = imf.for_mass(m_in_binaries_range) * (1.0 - constants.BIN_FRACTION)
    assert functions.imf_zero(m_in_binaries_range, imf) == imf_bin


def test_imf_binaries_are_zero_for_non_valid_masses():
    imf = select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)

    assert functions.imf_binary_primary(-1, imf) == 0.0
    assert functions.imf_binary_primary(constants.M_MIN / 2, imf) == 0.0
    assert functions.imf_binary_secondary(-1, imf) == 0.0
    assert functions.imf_binary_secondary(constants.B_MAX * 2, imf) == 0.0


def test_imf_binary_primary_integrates_phi_primary():
    m_in_binaries_range = 5.0
    m_sup = 2 * m_in_binaries_range
    imf = select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)

    expected = settings.default['binary_fraction'] * \
        functions.newton_cotes(m_in_binaries_range, m_sup, functions.phi_primary(m_in_binaries_range, imf))
    assert functions.imf_binary_primary(m_in_binaries_range, imf) == expected


def test_imf_binary_secondary_integrates_phi_secondary():
    m_in_binaries_range = 5.0
    m_inf = 2 * m_in_binaries_range
    imf = select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)

    expected = settings.default['binary_fraction'] * \
        functions.newton_cotes(m_inf, constants.B_MAX, functions.phi_secondary(m_in_binaries_range, imf))
    assert functions.imf_binary_secondary(m_in_binaries_range, imf) == expected


def test_global_imf():
    imf = select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)

    assert functions.global_imf(constants.M_MIN - 0.001, imf) == 0
    assert functions.global_imf(100, imf) == functions.imf_zero(100, imf)
    for m in [1, 4, 8, 10, 40]:
        assert 0 < functions.global_imf(m, imf)
        assert functions.imf_zero(100, imf) < functions.global_imf(m, imf)


def test_imf_supernovae_II_non_zero_for_SNII_masses():
    imf = select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)

    assert functions.imf_supernovae_II(constants.M_SNII + 0.01, imf) > 0
    assert functions.imf_supernovae_II(constants.M_SNII + np.random.sample() * 100, imf) > 0
    assert functions.imf_supernovae_II(constants.M_SNII + 100, imf) > 0


def test_imf_supernovae_II_is_zero_for_lower_masses():
    imf = select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)

    assert functions.imf_supernovae_II(np.random.sample() * constants.M_SNII, imf) == 0
    assert functions.imf_supernovae_II(constants.M_SNII, imf) == 0


def test_imf_supernovae_II_includes_binary_primaries():
    imf = select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)
    m = (constants.B_MIN + constants.B_MAX) / 2

    assert m > constants.M_SNII
    assert functions.imf_supernovae_II(m, imf) > functions.imf_zero(m, imf)/m


def test_return_fractions():
    imf = select_imf(np.random.choice(settings.valid_values["imf"]), settings.default)
    default_yields_file = settings.default['expelled_elements_filename']
    stellar_yields = elements.Expelled(default_yields_file)

    expected = functions.newton_cotes(
        1,
        100,
        lambda m:
            (functions.global_imf(m, imf)/m) * (m - stellar_yields.for_mass(m)['remnants'])
        )

    assert functions.return_fraction(1, 100, stellar_yields, imf) == expected
