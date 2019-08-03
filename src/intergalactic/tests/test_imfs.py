import pytest
import math
import numpy as np
import intergalactic.settings as settings
from intergalactic.imfs import select_imf, IMF
from intergalactic.imfs import Salpeter, Starburst, Chabrier, Ferrini, Kroupa, MillerScalo, Maschberger


@pytest.fixture
def available_imfs():
    """
    Fixture returning the names of all available IMFs defined in settings
    """
    return settings.valid_values["imf"]


def test_select_imf():
    strings = ["salpeter", "starburst", "chabrier", "ferrini", "kroupa", "miller_scalo", "maschberger"]
    classes = [Salpeter, Starburst, Chabrier, Ferrini, Kroupa, MillerScalo, Maschberger]

    for i in range(len(strings)):
        imf_instance = select_imf(strings[i])
        assert type(imf_instance) == classes[i]


def test_valid_values_presence(available_imfs):
    for imf in available_imfs:
        assert select_imf(imf) is not None


def test_description_presence(available_imfs):
    for imf in available_imfs:
        assert select_imf(imf).description() != IMF().description()


def test_salpeter_alpha():
    salpeter = Salpeter({"imf_alpha": 2.33})
    assert salpeter.alpha() == 2.33


def test_imf_is_zero_if_no_positive_mass(available_imfs):
    for imf in available_imfs:
        assert select_imf(imf).for_mass(0) == 0.0
        assert select_imf(imf).for_mass(-10) == 0.0

        for mass in [0.01, 0.02, 0.2, 0.75, 2, 8, 35, 90]:
            assert select_imf(imf).for_mass(mass) > 0.0


def test_minimum_mass_value_for_kroupa_imf():
    assert select_imf("kroupa").for_mass(0.009) == 0.0
    assert select_imf("kroupa").for_mass(0.01) > 0.0


def test_for_mass_is_normalized(available_imfs):
    for imf_name in available_imfs:
        imf = select_imf(imf_name)
        mass = np.random.random() * 10
        imf_for_mass = imf.for_mass(mass)
        assert imf_for_mass == imf.imf(mass) * imf.normalization_factor


def test_integration_accounts_for_mass_limits():
    imf_1 = IMF({"imf_m_low": 3, "imf_m_up": 103})
    imf_2 = IMF({"imf_m_low": 7, "imf_m_up": 57})
    assert imf_2.normalization_factor == 2 * imf_1.normalization_factor
    assert imf_1.integration_of_mass_interval() == 2 * imf_2.integration_of_mass_interval()
