#!/usr/bin/env python

import yaml
import numpy as np
import intergalactic.constants as constants
import intergalactic.settings as settings
import intergalactic.elements as elements
import intergalactic.functions as functions
import intergalactic.matrix as matrix
from intergalactic.functions import select_imf, select_abundances
from intergalactic.functions import mean_lifetime, stellar_mass, supernovas_a_rate, supernovas_b_rate
from intergalactic.functions import secondary_mass_fraction, total_energy_ejected
from intergalactic.functions import sn_rate_ruiz_lapuente, value_in_interval

def print_params(name, p):
  print("%s:"%name)
  for param in p:
    print("   " + str(param) + " = " + str(p[param]))
  print("**********************************")

with open("params.yml", "r") as params_file:
    input_params = yaml.safe_load(params_file)

settings = settings.validate(input_params)

print_params("Settings", settings)

initial_mass_function = select_imf(settings["imf"], settings)
print_params("IMF", {"initial_mass_function": initial_mass_function.description()})

abundances = select_abundances(settings["sol_ab"], float(settings["z"]))
print_params("Solar abundances (%s)" % abundances.description(), abundances.abundance())
settings["abundances"] = abundances


print_params("Binaries info", {"Fraction": constants.ALF, "Total integration time": constants.TTOT})

#[TEMP] AUX VARIABLES
imax1   = constants.IRID if constants.IC == 0 else constants.IMAX
tsep    = mean_lifetime(constants.MSEP, 0.02)
delt    = tsep / constants.LM2
delt1   = constants.LBLK * delt
lm1     = int(1 + (constants.LM2 * constants.TTOT) / (tsep * constants.LBLK))
bmaxm   = constants.BMAX / 2
sw      = (constants.NW - 1) / sum(constants.W)
w       = [i * sw for i in constants.W]

print("imax1 = " + str(imax1))
print("tsep = " + str(tsep))
print("delt = " + str(delt))
print("delt1 = " + str(delt1))
print("lm1 = " + str(lm1))
print("bmaxm = " + str(bmaxm))
print("sw = " + str(sw))
print("w = " + str(w))


# ETA Computation:  Proportion of stars with mass in [bmin, bmax] * alpha_bin_stars
# In the end ETA is the number of binary systems
eta = 0.0
cs  = settings["alpha_bin_stars"]
stm = (constants.BMAX - constants.BMIN) / (constants.NW - 1)

for i in range(0, constants.NW):
    bm = constants.BMIN + i * stm
    eta += w[i] * initial_mass_function.for_mass(bm) / bm

eta = cs * stm * eta
print("eta = " + str(eta))

print_params("Expelled elements for m=62", elements.Expelled().for_mass(62))


# Explosive nucleosynthesis:
mass_intervals, vna, vnb, et, sn_rate = [], [], [], [], []

mass_intervals_file = open("mass_intervals", "w")
line_1 = " ".join([str(i) for i in [constants.LM2, constants.LBLK, lm1]])
line_2 = " ".join([str(i) for i in [delt, lm1*delt1]])
mass_intervals_file.write("\n".join([line_1, line_2]))

supernovas_file = open("supernovas", "w")

m_inf = settings["m_max"]
t_sup = mean_lifetime(settings["m_max"], settings["z"])

for interval in range(1, constants.LM2 + 1):
    m_sup = m_inf
    m_inf = stellar_mass(delt * interval, settings["z"])
    m_inf = value_in_interval(m_inf, [constants.MSEP, settings["m_max"]])
    mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(interval))
    mass_intervals.append([m_inf, m_sup])

    t_inf = t_sup
    t_sup = delt * interval
    vna.append((supernovas_a_rate(t_sup) - supernovas_a_rate(t_inf)) * eta)
    vnb.append((supernovas_b_rate(t_sup) - supernovas_b_rate(t_inf)) * eta)

    et.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
    sn_rate.append(cs * 0.5 * (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)) * delt)

    supernovas_file.write(f'{interval}'.ljust(5)
                          + f'  {t_inf:.10f}'
                          + f'  {t_sup:.10f}'
                          + f'  {supernovas_a_rate(t_inf):.10f}'
                          + f'  {supernovas_b_rate(t_inf):.10f}'
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
    m_inf = stellar_mass(delt1 * interval, settings["z"])
    if m_inf >= constants.MSEP : m_inf = m_sup
    mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(interval))
    mass_intervals.append([m_inf, m_sup])

    t_sup = delt1 * interval
    if t_sup <= t_inf : t_sup = t_inf

    vna.append((supernovas_a_rate(t_sup) - supernovas_a_rate(t_inf)) * eta)
    vnb.append((supernovas_b_rate(t_sup) - supernovas_b_rate(t_inf)) * eta)

    et.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
    sn_rate.append(cs * 0.5 * (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)) * delt1)

    ii = constants.LM2 + interval
    supernovas_file.write(f'{ii}'.ljust(5)
                          + f'  {t_inf:.10f}'
                          + f'  {t_sup:.10f}'
                          + f'  {supernovas_a_rate(t_inf):.10f}'
                          + f'  {supernovas_b_rate(t_inf):.10f}'
                          + f'  {vna[ii - 1]:.10f}'
                          + f'  {vnb[ii - 1]:.10f}'
                          + f'  {sn_rate_ruiz_lapuente(t_inf):.10f}'
                          + f'  {sn_rate[ii - 1]:.11f}'
                          + '\n'
                         )

mass_intervals_file.close()
supernovas_file.close()

settings["expelled"] = elements.Expelled()

# Chandrasekhar limit = 1.4
feh = settings["abundances"].feh()
q_sn_ia = matrix.q_sn(1.4, feh, sn_type = "sn_ia")
q_sn_ib = matrix.q_sn(1.4, feh, sn_type = "sn_ib")
