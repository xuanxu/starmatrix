import pytest
import intergalactic.settings as settings

def test_defaults():
    assert settings.default != None
    for setting in ["z", "sol_ab", "imf", "imf_alpha",
        "m_max", "binary_fraction", "sn_ia_selection",
        "output_dir", "expelled_elements_filename"]:
        assert settings.default[setting] != None

def test_validate_with_valid_values():
    valid_values = {
        "z": 0.033,
        "imf": "miller_scalo",
        "sn_ia_selection": "tornambe",
        "sol_ab": "ag89",
        "m_max": 40.0,
        "output_dir": "testing"
    }

    params = settings.validate(valid_values)

    for param in ["z", "imf", "sn_ia_selection", "sol_ab", "m_max", "output_dir"]:
        assert params[param] == valid_values[param]

def test_validate_with_invalid_values():
    invalid_values = {
        "imf": "wrong name",
        "sn_ia_selection": "whatever",
        "sol_ab": "invalid",
        "m_max": 3.3
    }

    params = settings.validate(invalid_values)

    for param in ["imf", "sn_ia_selection", "sol_ab", "m_max"]:
        assert params[param] != invalid_values[param]
        assert params[param] == settings.default[param]
