import numpy as np
import intergalactic.constants as constants
import intergalactic.elements as elements
import intergalactic.matrix as matrix
from intergalactic.functions import select_imf, select_abundances
from intergalactic.functions import mean_lifetime, stellar_mass, supernovas_a_rate, supernovas_b_rate
from intergalactic.functions import total_energy_ejected, sn_rate_ruiz_lapuente, value_in_interval
from intergalactic.functions import imf_plus_primaries, imf_binary_secondary, imf_remnants
#from prettytable import PrettyTable

class Model:
    def __init__(self, settings = {}):
        self.context = settings
        self.init_variables()

    def init_variables(self):
        self.initial_mass_function = select_imf(self.context["imf"], self.context)
        self.context["abundances"] = select_abundances(self.context["sol_ab"], float(self.context["z"]))
        self.context["expelled"] = elements.Expelled()

        self.mass_intervals = []
        self.sn_a_rates = []
        self.sn_b_rates = []
        self.energies = []
        self.sn_rates = []

        tsep         = mean_lifetime(constants.MSEP, 0.02)
        self.delt    = tsep / constants.LM2
        self.delt1   = constants.LBLK * self.delt
        self.lm1     = int(1 + (constants.LM2 * constants.TTOT) / (tsep * constants.LBLK))
        self.bmaxm   = constants.BMAX / 2

    def run(self):

        self.eta = self.eta()
        self.explosive_nucleosynthesis()
        self.create_q_matrices()

    def create_q_matrices(self):
        # Chandrasekhar limit = 1.4
        feh = self.context["abundances"].feh()
        q_sn_ia = matrix.q_sn(1.4, feh, sn_type = "sn_ia")[0:15, 0:9]
        q_sn_ib = matrix.q_sn(1.4, feh, sn_type = "sn_ib")[0:15, 0:9]

        imf_sn_file = open(f"{self.context['output_dir']}/imf_supernova_rates", "w+")
        matrices_file =  open(f"{self.context['output_dir']}/qm-matrices", "w+")

        for i in range(0, constants.LM2 + self.lm1):
            m_inf, m_sup = self.mass_intervals[i]
            mass_step = (m_sup - m_inf) / (constants.N_INTERVALS)

            q = np.zeros((constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS))

            fik, fisik_a, fisik_b, fisiik = 0.0, 0.0, 0.0, 0.0
            sn_a_rates_k = 1e6 * self.sn_a_rates[i]
            sn_b_rates_k = 1e6 * self.sn_b_rates[i]
            energies_k  = 1e6 * self.energies[i]
            sn_rates_k = 1e6 * self.sn_rates[i]

            if m_sup > constants.MMIN and mass_step != 0:

                for ip in range(0, constants.N_POINTS):
                    m = m_inf +(mass_step * ip)
                    qm = matrix.q(m, self.context)[0:constants.Q_MATRIX_ROWS, 0:constants.Q_MATRIX_COLUMNS]

                    # Initial mass functions:
                    f = 1e6 * constants.WEIGHTS_N[ip] * mass_step
                    fm1 = f * imf_plus_primaries(m, self.initial_mass_function)
                    fm12 = fm1 + f * imf_binary_secondary(m, self.initial_mass_function, SNI_events = False)
                    # fmr = f * imf_remnants(m, self.initial_mass_function, self.context["expelled"])
                    fik += fm12
                    if m > constants.MSN2 : fisiik += fm1/m

                    if self.context["sn_ia_selection"] == "matteucci":
                        fm2s = f * imf_binary_secondary(m, self.initial_mass_function, SNI_events = True)
                        fisik_a += fm2s/m
                        fisik_b = 0
                    elif self.context["sn_ia_selection"] == "tornambe":
                        fisik_a = sn_a_rates_k
                        fisik_b = sn_b_rates_k
                    elif self.context["sn_ia_selection"] == "rlp":
                        fisik_a = sn_rates_k
                        fisik_b = 0

                    q += fm12 * qm

                    if m < self.bmaxm:
                       q += (fisik_a * q_sn_ia) + (fisik_b * q_sn_ib)

            np.savetxt(matrices_file, q, fmt="%15.8f", header=f"Q matrix for mass interval: [{m_sup}, {m_inf}]")
            imf_sn_file.write(f'{fik:.4f}'
                              + f'  {fisiik:.4f}'
                              + f'  {fisik_a:.4f}'
                              + f'  {fisik_b:.4f}'
                              + f'  {sn_b_rates_k:.4f}'
                              + f'  {energies_k:.4f}'
                              + '\n'
                             )

        matrices_file.close()
        imf_sn_file.close()

    def eta(self):
        # ETA Computation:  Proportion of stars with mass in [bmin, bmax] * alpha_bin_stars
        # In the end ETA is the number of binary systems
        eta = 0.0
        stm = (constants.BMAX - constants.BMIN) / (constants.N_INTERVALS)

        for i in range(0, constants.N_POINTS):
            bm = constants.BMIN + i * stm
            eta += constants.WEIGHTS_N[i] * self.initial_mass_function.for_mass(bm) / bm

        return self.context["alpha_bin_stars"] * stm * eta

    def explosive_nucleosynthesis(self):

        mass_intervals_file = open(f"{self.context['output_dir']}/mass_intervals", "w+")
        line_1 = " ".join([str(i) for i in [constants.LM2, constants.LBLK, self.lm1]])
        line_2 = " ".join([str(i) for i in [self.delt, self.lm1*self.delt1]])
        mass_intervals_file.write("\n".join([line_1, line_2]))

        m_inf = self.context["m_max"]
        t_sup = mean_lifetime(self.context["m_max"], self.context["z"])

        for interval in range(1, constants.LM2 + 1):
            m_sup = m_inf
            m_inf = stellar_mass(self.delt * interval, self.context["z"])
            m_inf = value_in_interval(m_inf, [constants.MSEP, self.context["m_max"]])
            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(interval))
            self.mass_intervals.append([m_inf, m_sup])

            t_inf = t_sup
            t_sup = self.delt * interval
            self.sn_a_rates.append((supernovas_a_rate(t_sup) - supernovas_a_rate(t_inf)) * self.eta)
            self.sn_b_rates.append((supernovas_b_rate(t_sup) - supernovas_b_rate(t_inf)) * self.eta)

            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_rates.append(self.context["alpha_bin_stars"] * 0.5 *
                (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)) * self.delt)

        m_inf = constants.MSEP
        for interval in range(1, self.lm1 + 1):
            m_sup = m_inf
            t_inf = t_sup
            m_inf = stellar_mass(self.delt1 * interval, self.context["z"])
            if m_inf >= constants.MSEP : m_inf = m_sup
            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(interval))
            self.mass_intervals.append([m_inf, m_sup])

            t_sup = self.delt1 * interval
            if t_sup <= t_inf : t_sup = t_inf

            self.sn_a_rates.append((supernovas_a_rate(t_sup) - supernovas_a_rate(t_inf)) * self.eta)
            self.sn_b_rates.append((supernovas_b_rate(t_sup) - supernovas_b_rate(t_inf)) * self.eta)

            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_rates.append(self.context["alpha_bin_stars"] * 0.5 *
                (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)) * self.delt1)

            ii = constants.LM2 + interval

        mass_intervals_file.close()
