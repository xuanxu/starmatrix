"""
Default settings and initial parameters

All the values set here can be overwritten via the input file: params.yml

"""
from os.path import dirname, join
from intergalactic import constants as constants

default = {
    "z": 0.02,
    "sol_ab": "as09",
    "imf": "kroupa",
    "imf_alpha": 2.35,
    "m_max": 40.0,
    "binary_fraction": constants.BIN_FRACTION,
    "sn_ia_selection": "rlp",
    "output_dir": "results",
    "expelled_elements_filename":  join(dirname(__file__),"sample_input", "expelled_elements")
}


valid_values = {
    "imf": ["salpeter", "chabrier", "ferrini", "kroupa", "miller_scalo", "starburst", "maschberger"],
    "sn_ia_selection": ["matteucci", "tornambe", "rlp"],
    "sol_ab": ["ag89", "gs98", "as05", "as09", "he10"],
    "m_max": [40.0, 100.0]
}

def validate(params):
    params = {**default, **params}
    for param in valid_values.keys():
        if params[param] not in valid_values[param]:
            print(f"Provided value for {param} is incorrect.")
            print(f"  Valid values for {param} are: {valid_values[param]}")
            print(f"  Using default value: {default[param]}")
            params[param] = default[param]

    return params