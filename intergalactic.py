#!/usr/bin/env python

import json
from intergalactic.functions import select_imf, abundances
from intergalactic.functions import tau, effe, emme, ennea, enneb, etout
from intergalactic.functions import sn_rate_ruiz_lapuente, value_in_interval
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

settings = {**settings.default, **input_params}
settings["m_max"] = constants.MMAX
if settings["massive_yields"] in ["WOW", "CLI", "KOB"]:
    settings["m_max"] = settings["imf_m_up"]

print_params("Settings", settings)

initial_mass_function = select_imf(settings["imf"], settings)
print_params("IMF", {"initial_mass_function": initial_mass_function.description()})

abundances = abundances(settings["sol_ab"], float(settings["z"]))
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
sw      = (constants.NW - 1) / sum(constants.W)
w       = [i * sw for i in constants.W]

print("imax1 = " + str(imax1))
print("tsep = " + str(tsep))
print("delt = " + str(delt))
print("delt1 = " + str(delt1))
print("lm1 = " + str(lm1))
print("bmaxm = " + str(bmaxm))
print("umalf = " + str(umalf))
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


# Explosive nucleosynthesis:
mass_intervals, vna, vnb, et, sn_rate = [], [], [], [], []

mass_intervals_file = open("mass_intervals", "w")
line_1 = " ".join([str(i) for i in [constants.LM2, constants.LBLK, lm1]])
line_2 = " ".join([str(i) for i in [delt, lm1*delt1]])
mass_intervals_file.write("\n".join([line_1, line_2]))

supernovas_file = open("supernovas", "w")

m_inf = settings["m_max"]
t_sup = tau(settings["m_max"], settings["z"])

for interval in range(1, constants.LM2 + 1):
    m_sup = m_inf
    m_inf = emme(delt * interval, settings["z"])
    m_inf = value_in_interval(m_inf, [constants.MSEP, settings["m_max"]])
    mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(interval))
    mass_intervals.append([m_inf, m_sup])

    t_inf = t_sup
    t_sup = delt * interval
    vna.append((ennea(t_sup) - ennea(t_inf)) * eta)
    vnb.append((enneb(t_sup) - enneb(t_inf)) * eta)

    et.append(etout(t_sup) - etout(t_inf))
    sn_rate.append(cs * 0.5 * (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)) * delt)

    supernovas_file.write(f'{interval}'.ljust(5)
                          + f'  {t_inf:.10f}'
                          + f'  {t_sup:.10f}'
                          + f'  {ennea(t_inf):.10f}'
                          + f'  {enneb(t_inf):.10f}'
                          + f'  {vna[interval - 1]:.10f}'
                          + f'  {vnb[interval - 1]:.10f}'
                          + f'  {sn_rate_ruiz_lapuente(t_inf):.10f}'
                          + f'  {sn_rate[interval - 1]:.10f}'
                          + '\n'
                         )

m_inf = constants.MSEP
for interval in range(1, lm1 + 1):
    m_sup = m_inf
    t_inf = t_sup
    m_inf = emme(delt1 * interval, settings["z"])
    if m_inf >= constants.MSEP : m_inf = m_sup
    mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(interval))
    mass_intervals.append([m_inf, m_sup])

    t_sup = delt1 * interval
    if t_sup <= t_inf : t_sup = t_inf

    vna.append((ennea(t_sup) - ennea(t_inf)) * eta)
    vnb.append((enneb(t_sup) - enneb(t_inf)) * eta)

    et.append(etout(t_sup) - etout(t_inf))
    sn_rate.append(cs * 0.5 * (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)) * delt1)

    ii = constants.LM2 + interval
    supernovas_file.write(f'{ii}'.ljust(5)
                          + f'  {t_inf:.10f}'
                          + f'  {t_sup:.10f}'
                          + f'  {ennea(t_inf):.10f}'
                          + f'  {enneb(t_inf):.10f}'
                          + f'  {vna[ii - 1]:.10f}'
                          + f'  {vnb[ii - 1]:.10f}'
                          + f'  {sn_rate_ruiz_lapuente(t_inf):.10f}'
                          + f'  {sn_rate[ii - 1]:.11f}'
                          + '\n'
                         )


mass_intervals_file.close()
supernovas_file.close()
