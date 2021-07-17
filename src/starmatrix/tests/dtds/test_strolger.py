import pytest
from starmatrix.dtds import Strolger


def test_parameters_initialization():
    strolger = Strolger(1000, 2000, 3000)
    assert strolger.psi == 1000
    assert strolger.omega == 2000
    assert strolger.alpha == 3000


def test_has_description():
    assert Strolger(10, 10, 10).description() is not None


def test_is_normalized():
    dtd = Strolger(6000, 6000, -2)
    sample_t = 6
    dtd_point = dtd.at_time(sample_t)
    assert dtd_point > 0
    assert dtd_point == dtd.phi(sample_t) * dtd.normalization_rate()


def test_normalization_rate_uses_hubble_efficiency():
    dtd = Strolger(6000, 6000, -2)
    assert dtd.normalization_rate() == 1.03e-3 / dtd.phi_integrated()
