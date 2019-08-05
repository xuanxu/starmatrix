import pytest
import math
import numpy as np
from intergalactic.elements import Expelled
import intergalactic.settings as settings


@pytest.fixture
def expelled():
    """
    Fixture returning a Expelled instance initialized with the default expelled data file
    """
    expelled = Expelled(settings.default["expelled_elements_filename"])
    return expelled


def test_read_file_on_init(expelled):
    assert len(expelled.mass_points) == 80
    assert expelled.mass_points[0] == 0.8
    assert expelled.mass_points[-1] == 100
    assert len(expelled.by_mass[0.8]) == len(expelled.elements_list)


def test_interpolation_for_mass_data(expelled):
    i = np.random.randint(0, len(expelled.mass_points)-1)

    m_low = expelled.mass_points[i]
    m_up = expelled.mass_points[i + 1]
    m = m_low + 0.5 * (m_up - m_low)

    expelled_for_mass = expelled.for_mass(m)

    for element in expelled.elements_list:
        interval = sorted([expelled.by_mass[m_up][element] / m, expelled.by_mass[m_low][element] / m])

        assert expelled_for_mass[element] <= interval[1]
        assert expelled_for_mass[element] >= interval[0]


def test_extrapolation_for_mass_data(expelled):
    m_low = expelled.mass_points[-2]
    m_up = expelled.mass_points[-1]
    last_step_data_size = m_up - m_low

    m = m_up + last_step_data_size

    expelled_for_mass = expelled.for_mass(m)

    for element in expelled.elements_list:
        by_mass_m_up = expelled.by_mass[m_up][element]
        by_mass_m_low = expelled.by_mass[m_low][element]
        extrapolation = by_mass_m_up + (by_mass_m_up - by_mass_m_low)

        assert expelled_for_mass[element] == extrapolation / m
