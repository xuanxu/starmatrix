import pytest
import intergalactic.settings as settings
from intergalactic.functions import max_mass_allowed

def test_defaults():
    assert settings.default != None
    for setting in ["z", "sol_ab", "imf", "imf_alpha",
        "m_max", "binary_fraction", "dtd_sn",
        "output_dir", "expelled_elements_filename"]:
        assert settings.default[setting] != None

def test_validate_with_valid_values():
    valid_values = {
        "z": 0.033,
        "imf": "miller_scalo",
        "dtd_sn": "mdvp",
        "sol_ab": "ag89",
        "m_max": 40.0,
        "output_dir": "testing"
    }

    params = settings.validate(valid_values)

    for param in ["z", "imf", "dtd_sn", "sol_ab", "m_max", "output_dir"]:
        assert params[param] == valid_values[param]

def test_validate_with_invalid_values():
    invalid_values = {
        "imf": "wrong name",
        "dtd_sn": "whatever",
        "sol_ab": "invalid",
        "m_max": 3.3
    }

    params = settings.validate(invalid_values)

    for param in ["imf", "dtd_sn", "sol_ab"]:
        assert params[param] != invalid_values[param]
        assert params[param] == settings.default[param]

def test_validate_max_mass_with_valid_values():
    params = settings.validate({"m_max": 33})
    assert params["m_max"] == 33

def test_validate_max_mass_with_invalid_values():
    for z in [0.001, 0.008, 0.2, 0.33, 0.5]:
        params = settings.validate({"m_max": 300, "z": z})
        assert params["m_max"] == max_mass_allowed(z)
