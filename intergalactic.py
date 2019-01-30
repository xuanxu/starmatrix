#!/usr/bin/env python

import json
from intergalactic.functions import select_imf, abundances
from intergalactic.functions import tau
import intergalactic.constants as constants
import intergalactic.settings as settings

def print_params(name, p):
  #print("**********************************")
  print("%s:"%name)
  for param in p:
    print("   " + str(param) + " = " + str(p[param])[:80])
  print("**********************************")

with open("params.json", "r") as params_file:
    input_params = json.load(params_file)

#py > 3.5: {**settings.default, **input_params}
settings = settings.default.copy()
settings.update(input_params) 
if settings["massive_yields"] in ["WOW", "CLI", "KOB"]:
    settings["m_max"] = settings["imf_m_up"]

print_params("Settings", settings)

initial_mass_function = select_imf(settings["imf"], input_params)
print_params("IMF", {"initial_mass_function": initial_mass_function.description()})

abundances = abundances(input_params["sol_ab"], float(input_params["z"]))
elements=abundances.abundance()
print_params("Solar abundances (%s)" % abundances.description(), elements)

print_params("Binaries info", {"Fraction": constants.ALF, "Gamma": constants.GAMMA, "Total integration time": constants.TTOT})

#[TEMP] AUX VARIABLES
imax1   = constants.IRID if constants.IC == 0 else constants.IMAX
tsep    = tau(constants.MSEP, 0.02)
delt    = tsep / constants.LM2
delt1   = constants.LBLK * delt
lm1     = int(1 + (constants.LM2 * constants.TTOT) / (tsep * constants.LBLK))
bmaxm   = constants.BMAX / 2
umalf   = 1.0 - constants.ALF
costfmu = (1.0 + constants.GAMMA) * 2.0 ** (1.0 + constants.GAMMA)
sw      = (constants.NW - 1) / sum(constants.W)
w       = [i * sw for i in constants.W]

print("imax1 = " + str(imax1))
print("tsep = " + str(tsep))
print("delt = " + str(delt))
print("delt1 = " + str(delt1))
print("lm1 = " + str(lm1))
print("bmaxm = " + str(bmaxm))
print("umalf = " + str(umalf))
print("costfmu = " + str(costfmu))
print("sw = " + str(sw))
print("w = " + str(w))


# ETA Computation:  Proportion of stars with mass in [bmin, bmax] * alpha_bin_stars
# In the end ETA is the number of binary systems
eta = 0.0
cs  = settings["alpha_bin_stars"]
stm = (constants.BMAX - constants.BMIN) / (constants.NW - 1)
# for 1=1:nw
for i in range(0, constants.NW):
    bm = constants.BMIN + i * stm
    eta += w[i] * initial_mass_function.for_mass(bm) / bm

eta = cs * stm * eta
print("eta = " + str(eta))

# Read ejected masses file. By mass (1st column) 
ejected_elements_names = ["h", "d", "he3", "he4", "c12", "o16", "n14p", "c13", "n.r.", "ne", "mg", "si", "s", "ca", "fe", "remanents", "c13s", "n14s"]
ejected_masses = {}
ejected_data = open("exp", "r")
for line in ejected_data:
    data_row = [float(data) for data in line.split()]
    data_row = [0.0 if data < 0 else data for data in data_row]
    mass = data_row.pop(0) # the first column is the mass

    ejected_masses[mass] = dict(zip(ejected_elements_names, data_row))
ejected_data.close()
#print_params("Ejected masses", ejected_masses)


