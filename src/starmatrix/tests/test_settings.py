import pytest
import starmatrix.settings as settings
from starmatrix.functions import max_mass_allowed


def test_defaults():
    assert settings.default is not None
    for setting in ["z", "sol_ab", "imf", "imf_alpha",
                    "m_max", "binary_fraction", "dtd_sn", "sn_yields",
                    "output_dir", "expelled_elements_filename"]:
        assert settings.default[setting] is not None


def test_default_settings_with_no_params():
    assert settings.default_settings() == settings.default_settings(settings.default)


def test_default_settings_adds_extra_params():
    test_settings = {"integration_step": "fixed_n_steps"}
    expected_values = settings.default_extraparams["integration_step"]["fixed_n_steps"]
    complete_default_settings = settings.default_settings(test_settings)

    for k in ["integration_steps_stars_bigger_than_4Msun", "integration_steps_stars_smaller_than_4Msun"]:
        assert (k in settings.default) is False
        assert (k in complete_default_settings) is True
        assert complete_default_settings[k] == expected_values[k]


def test_default_settings_adds_extra_params_only_if_needed():
    settings.default_extraparams["inexistent_setting"] = {"a": 34}
    params = settings.default_settings({"integration_step": "testing"})
    assert(params) == settings.default
    assert("inexistent_setting" in params) is False


def test_validate_with_valid_values():
    valid_values = {
        "z": 0.033,
        "imf": "miller_scalo",
        "imf_m_low": 0.3,
        "dtd_sn": "castrillo",
        "sol_ab": "ag89",
        "sn_yields": "iwa1998",
        "m_max": 40.0,
        "output_dir": "testing"
    }

    params = settings.validate(valid_values)

    for param in ["z", "imf", "imf_m_low", "dtd_sn", "sol_ab", "m_max", "output_dir"]:
        assert params[param] == valid_values[param]


def test_validate_with_invalid_values():
    invalid_values = {
        "imf": "wrong name",
        "dtd_sn": "whatever",
        "sol_ab": "invalid",
        "sn_yields": "incorrect",
        "m_max": 3.3
    }

    params = settings.validate(invalid_values)

    for param in ["imf", "dtd_sn", "sol_ab", "sn_yields"]:
        assert params[param] != invalid_values[param]
        assert params[param] == settings.default[param]


def test_validate_max_mass_with_valid_values():
    params = settings.validate({"m_max": 33})
    assert params["m_max"] == 33


def test_validate_max_mass_with_invalid_values():
    for z in [0.001, 0.008, 0.2, 0.33, 0.5]:
        params = settings.validate({"m_max": 300, "z": z})
        assert params["m_max"] == max_mass_allowed(z)


def test_validate_mass_limits_for_starburst_imf():
    for imf in settings.valid_values["imf"]:
        params = settings.validate({"imf": imf, "imf_m_low": 7, "imf_m_up": 40})
        if imf == "starburst":
            assert params["imf_m_low"] == 1
            assert params["imf_m_up"] == 120
        else:
            assert params["imf_m_low"] == 7
            assert params["imf_m_up"] == 40


def test_validate_with_invalid_settings():
    params = settings.validate({"imf_m_low": 7, "invalid_setting": 47})

    assert(params["imf_m_low"]) == 7
    assert("invalid_setting" in params) is False


def test_validate_with_yield_corrections():
    params = settings.validate({"yield_corrections": {"Mg": 3, "Aluminium": 4}})
    assert(params["yield_corrections"]) == {"Mg": 3}


def test_validate_yield_corrections_with_invalid_input():
    no_dict_input = settings.validate_yield_corrections([])
    invalid_value_input = settings.validate_yield_corrections({"H": "A lot"})

    assert(no_dict_input) == {}
    assert(invalid_value_input) == {}


def test_validate_yield_corrections():
    corrections = {"H": 1.3, "mg": 2.1, "fE": 4, "AllTheRest": 7.8, "Si": "Wrong"}
    valid_corrections = settings.validate_yield_corrections(corrections)

    assert(valid_corrections) == {"H": 1.3, "Mg": 2.1, "Fe": 4}


def test_deprecation_warnings():
    dw = settings.deprecation_warnings({"deprecation_warnings": False})
    assert len(dw) == 0

    dw = settings.deprecation_warnings({"deprecation_warnings": "test"})
    assert len(dw) == 1
