#!/usr/bin/env python

import json
from intergalactic.functions import select_imf, abundances
import intergalactic.constants as constants
import intergalactic.settings as settings

def print_params(name, p):
  #print("**********************************")
  print("%s:"%name)
  for param in p:
    print("   " + param + " = " + str(p[param]))
  print("**********************************")

with open("params.json", "r") as params_file:
    input_params = json.load(params_file)

settings = input_params # merge with**defaults
if settings["massive_yields"] in ["WOW", "CLI", "KOB"]:
    settings["m_max"] = settings["imf_m_up"]

print_params("Settings", settings)

initial_mass_function = select_imf(settings["imf"], input_params)
print_params("IMF", {"initial_mass_function": initial_mass_function.description()})

solar_abundances = abundances(input_params["sol_ab"], float(input_params["z"]))
print_params("Solar abundances", solar_abundances)

print_params("Binaries info", {"Fraction": constants.ALF, "Gamma": constants.GAMMA, "Total integration time": constants.TTOT})







