import pytest
import math
import numpy as np
import intergalactic.settings as settings
from intergalactic.imfs import select_imf, IMF
from intergalactic.imfs import Salpeter, Starburst, Chabrier, Ferrini, Kroupa, MillerScalo, Maschberger

@pytest.fixture
def available_imfs():
    return settings.valid_values["imf"]

def test_select_imf():
    strings = ["salpeter", "starburst", "chabrier", "ferrini", "kroupa", "miller_scalo", "maschberger"]
    classes = [Salpeter, Starburst, Chabrier, Ferrini, Kroupa, MillerScalo, Maschberger]

    for i in range(len(strings)):
        imf_instance = select_imf(strings[i])
        assert type(imf_instance) == classes[i]

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
