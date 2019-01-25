#!/usr/bin/env python

import json
from sys import exit
from intergalactic.functions import select_imf, abundances

def print_params(name, p):
  print("**********************************")
  print("%s:"%name)
  for param in p:
    print("   " + param + " = " + str(p[param]))
  print("**********************************")



with open("params.json", "r") as params_file:
    input_params = json.load(params_file)
    print_params("Input params", input_params)


imf_options = [
               "salpeter",
               "miller_scalo",
               "ferrini",
               "starburst",
               "kroupa",
               "chabrier",
               "maschberger"
              ]


for option in imf_options:
    i = select_imf(option, input_params)
    print(i.description())
    print(i.for_mass(0.01))
    print(i.for_mass(0.6))
    print(i.for_mass(5))
    print(i.for_mass(42))
    print("___________________________")


solar_abundances = abundances(input_params["sol_ab"], float(input_params["z"]))
print_params("Abundancias solares", solar_abundances)






