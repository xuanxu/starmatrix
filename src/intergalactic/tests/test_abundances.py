import pytest
import numpy as np
import intergalactic.functions as functions
import intergalactic.settings as settings
from intergalactic.abundances import Abundances

@pytest.fixture
def available_abundances():
    return settings.valid_values["sol_ab"]

def test_abundances_classes_presence(available_abundances):
    for abundance in available_abundances:
        assert functions.select_abundances(abundance, 0.02) != None

def test_description_presence(available_abundances):
    for abundance in available_abundances:
        assert functions.select_abundances(abundance, 0.02).description() != Abundances(0.02).description()

def test_feh_with_z_zero():
    assert Abundances(0).feh() == -20

def test_feh_with_z_non_zero(available_abundances):
    for abundance in available_abundances:
        assert functions.select_abundances(abundance, 0.025).feh() > 0.0

def test_h_he4_values(available_abundances):
    for abundance in available_abundances:
        assert functions.select_abundances(abundance, 0.025).h() > 0.0
        assert functions.select_abundances(abundance, 0.025).he4() > 0.0

def test_elements_value_presence(available_abundances):
    for abundance in available_abundances:
        elements = np.array(list(functions.select_abundances(abundance, 0.025).elements().values()))
        assert np.all(elements > 0.0)
        assert np.all(elements < 1.0)

def test_abundance_values_presence(available_abundances):
    for abundance in available_abundances:
        abundance_values = np.array(list(functions.select_abundances(abundance, 0.025).abundance().values()))
        assert np.all(abundance_values > 0.0)
