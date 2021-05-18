"""
Default settings and initial parameters

All the values set here can be overwritten via the input file: params.yml

"""
from os.path import dirname, join
from starmatrix import constants as constants
from starmatrix import elements
from starmatrix.functions import max_mass_allowed

default = {
    "z": 0.02,
    "sol_ab": "as09",
    "imf": "kroupa",
    "imf_alpha": 2.35,
    "imf_m_low": 0.15,
    "imf_m_up": 100,
    "m_min": 0.98,
    "m_max": 40.0,
    "binary_fraction": constants.BIN_FRACTION,
    "dtd_sn": "rlp",
    "dtd_correction_factor": 1.0,
    "sn_yields": "iwa1998",
    "output_dir": "results",
    "matrix_headers": True,
    "return_fractions": False,
    "integration_step": "logt",
    "deprecation_warnings": True,
    "expelled_elements_filename": join(dirname(__file__), "sample_input", "expelled_elements"),
    "yield_corrections": {},
}

valid_values = {
    "imf": ["salpeter", "starburst", "chabrier", "ferrini", "kroupa", "miller_scalo", "maschberger"],
    "dtd_sn": ["rlp", "maoz", "castrillo", "greggio", "chen", "greggio-CDD04", "greggio-CDD1",
               "greggio-WDD04", "greggio-WDD1", "greggio-SDCH", "greggio-SDSCH"],
    "sn_yields": ["iwa1998",
                  "sei2013",
                  "ln2020",
                  "ln2018-1", "ln2018-2", "ln2018-3",
                  "br2019-1", "br2019-2",
                  "gro2021-1", "gro2021-2",
                  "mor2018-1", "mor2018-2"],
    "sol_ab": ["ag89", "gs98", "as05", "as09", "he10", "lo19"],
    "integration_step": ["logt", "t", "two_steps_t", "fixed_n_steps"],
}

default_extraparams = {
    "integration_step": {
        "fixed_n_steps": {
            "integration_steps_stars_bigger_than_4Msun": 150,
            "integration_steps_stars_smaller_than_4Msun": 90
        },
        "logt": {
            "total_time_steps": 300,
        },
        "t": {
            "total_time_steps": 300,
        }
    }
}


def default_settings(params=default):
    default_params = default
    params = {**default_params, **params}

    for extraparam in default_extraparams.keys():
        if extraparam in params:
            if params[extraparam] in default_extraparams[extraparam].keys():
                default_params = {**default_params, **default_extraparams[extraparam][params[extraparam]]}

    return default_params


def validate(params):
    default_params = default_settings(params)
    params = {**default_params, **params}

    for param in valid_values.keys():
        if params[param] not in valid_values[param]:
            print(f"Provided value for {param} is incorrect.")
            print(f"  Valid values for {param} are: {valid_values[param]}")
            print(f"  Using default value: {default_params[param]}")
            params[param] = default_params[param]

    if params["m_max"] > max_mass_allowed(params["z"]):
        params["m_max"] = max_mass_allowed(params["z"])
        print(f"Maximum mass is bigger than the allowed mass for z: {params['z']}")
        print(f"  Using m_max value: {params['m_max']} solar masses")

    if params["imf"] == "starburst":
        params["imf_m_low"] = 1.0
        params["imf_m_up"] = 120.0

    if params["yield_corrections"] == {}:
        params.pop("yield_corrections")
    else:
        params["yield_corrections"] = validate_yield_corrections(params["yield_corrections"])

    invalid_params = params.keys() - default_params.keys()
    for invalid_param in invalid_params:
        print(f"Ignoring invalid setting: {invalid_param}")
        params.pop(invalid_param)

    print("")
    deprecation_warnings(params)

    return params


def validate_yield_corrections(corrections):
    valid_corrections = {}
    valid_elements = elements.Expelled.elements_list
    if type(corrections) is not dict:
        print("Yield corrections ignored")
        print("  Invalid format, it should be a dict of element: value pairs")
        print("  Valid values for element are: ")
        print(f"  {', '.join(valid_elements)}")
        print("")
        return valid_corrections

    normalized_input_corrections = dict((k.lower(), v) for k, v in corrections.items())

    for element in valid_elements:
        if element.lower() in normalized_input_corrections:
            value = normalized_input_corrections[element.lower()]
            if type(value) == int or type(value) == float:
                valid_corrections[element] = value
            else:
                print(f"Yield correction for {element} ignored: is not a number")

    invalid_corrections = normalized_input_corrections.keys() - [e.lower() for e in valid_elements]
    for invalid_correction in invalid_corrections:
        print(f"Yield correction for {invalid_correction} ignored: Invalid element")

    return valid_corrections


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
