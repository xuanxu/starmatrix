import pytest
import math
import numpy as np
import intergalactic.functions as functions
import intergalactic.settings as settings
from intergalactic.imfs import IMF, Salpeter, Maschberger

@pytest.fixture
def available_imfs():
    return settings.valid_values["imf"]

def test_description_presence(available_imfs):
    for imf in available_imfs:
        assert functions.select_imf(imf).description() != IMF().description()

def test_salpeter_alpha():
    salpeter = Salpeter({"imf_alpha": 2.33})
    assert salpeter.alpha() == 2.33

def test_imf_is_zero_if_no_positive_mass(available_imfs):
    for imf in available_imfs:
        assert functions.select_imf(imf).for_mass(0) == 0.0
        assert functions.select_imf(imf).for_mass(-10) == 0.0

def test_for_mass(available_imfs):
    for imf in available_imfs:
        assert functions.select_imf(imf).for_mass(np.random.random()*10) > 0.0
