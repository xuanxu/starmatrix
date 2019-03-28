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
    "m_min": 0.98,
    "m_max": 40.0,
    "total_time_steps": 300,
    "binary_fraction": constants.BIN_FRACTION,
    "dtd_sn": "rlp",
    "output_dir": "results",
    "expelled_elements_filename":  join(dirname(__file__),"sample_input", "expelled_elements")
}

valid_values = {
    "imf": ["salpeter", "chabrier", "ferrini", "kroupa", "miller_scalo", "starburst", "maschberger"],
    "dtd_sn": ["rlp", "mdvp"],
    "sol_ab": ["ag89", "gs98", "as05", "as09", "he10"],
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
        print(f"Maximum mass is bigger than the allowewd mass for z = : {params['z']}")
        print(f"  Using m_max value: {params['m_max']} solar masses")

    return params