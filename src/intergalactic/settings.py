"""
Default settings and initial parameters

All the values set here can be overwritten via the input file: params.yml

"""
from os.path import dirname, join
from intergalactic import constants as constants
from intergalactic.functions import max_mass_allowed

default = {
    "z": 0.02,
    "sol_ab": "as09",
    "imf": "kroupa",
    "imf_alpha": 2.35,
    "imf_m_low": 0.15,
    "imf_m_up": 100,
    "m_min": 0.98,
    "m_max": 40.0,
    "total_time_steps": 300,
    "binary_fraction": constants.BIN_FRACTION,
    "dtd_sn": "rlp",
    "output_dir": "results",
    "matrix_headers": True,
    "return_fractions": False,
    "integration_step": "logt",
    "deprecation_warnings": True,
    "expelled_elements_filename": join(dirname(__file__), "sample_input", "expelled_elements")
}

valid_values = {
    "imf": ["salpeter", "starburst", "chabrier", "ferrini", "kroupa", "miller_scalo", "maschberger"],
    "dtd_sn": ["rlp", "maoz", "castrillo", "greggio"],
    "sol_ab": ["ag89", "gs98", "as05", "as09", "he10", "lo19"],
    "integration_step": ["logt", "t", "two_steps_t", "fixed_n_steps"],
}


def validate(params):
    params = {**default, **params}
    for param in valid_values.keys():
        if params[param] not in valid_values[param]:
            print(f"Provided value for {param} is incorrect.")
            print(f"  Valid values for {param} are: {valid_values[param]}")
            print(f"  Using default value: {default[param]}")
            params[param] = default[param]

    if params["m_max"] > max_mass_allowed(params["z"]):
        params["m_max"] = max_mass_allowed(params["z"])
        print(f"Maximum mass is bigger than the allowed mass for z: {params['z']}")
        print(f"  Using m_max value: {params['m_max']} solar masses")

    if params["imf"] == "starburst":
        params["imf_m_low"] = 1.0
        params["imf_m_up"] = 120.0

    deprecation_warnings(params)

    return params


def deprecation_warnings(params):
    deprecation_warnings = []

    if params["deprecation_warnings"] is False:
        return []

    if params["deprecation_warnings"] == "test":
        deprecation_warnings.append("Deprecation warnings show here.")

    if deprecation_warnings:
        print("*** Deprecations Warning ***")
        for msg in deprecation_warnings:
            print("!! " + msg)
        print("")

    return deprecation_warnings
