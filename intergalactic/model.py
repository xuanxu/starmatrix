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
        self.vna = []
        self.vnb = []
        self.et = []
        self.sn_rate = []

        self.imax1   = constants.IRID if constants.IC == 0 else constants.IMAX
        self.tsep    = mean_lifetime(constants.MSEP, 0.02)
        self.delt    = self.tsep / constants.LM2
        self.delt1   = constants.LBLK * self.delt
        self.lm1     = int(1 + (constants.LM2 * constants.TTOT) / (self.tsep * constants.LBLK))
        self.bmaxm   = constants.BMAX / 2
        sw           = (constants.NW - 1) / sum(constants.W)
        self.w       = [i * sw for i in constants.W]

    def run(self):

        self.eta = self.eta()
        self.explosive_nucleosynthesis()
        self.create_q_matrices()

    def create_q_matrices(self):
        # Chandrasekhar limit = 1.4
        feh = self.context["abundances"].feh()
        q_sn_ia = matrix.q_sn(1.4, feh, sn_type = "sn_ia")[0:15, 0:9]
        q_sn_ib = matrix.q_sn(1.4, feh, sn_type = "sn_ib")[0:15, 0:9]

        imf_sn_file = open(f"imf_supernova_rates", "w")
        for i in range(0, constants.LM2 + self.lm1):
            m_inf, m_sup = self.mass_intervals[i]
            mass_step = (m_sup - m_inf) / (constants.NW - 1)

            q = np.zeros((self.imax1, constants.JMAX))

            fik, fisik_a, fisik_b, fisiik = 0.0, 0.0, 0.0, 0.0
            vnak = 1e6 * self.vna[i]
            vnbk = 1e6 * self.vnb[i]
            etk  = 1e6 * self.et[i]
            sn_ratek = 1e6 * self.sn_rate[i]

            if m_sup > constants.MMIN and mass_step != 0:

                for ip in range(0, constants.NW):
                    m = m_inf +(mass_step * ip)
                    qm = matrix.q(m, self.context)[0:15, 0:9]

                    # Initial mass functions:
                    f = 1e6 * self.w[ip] * mass_step
                    fm1 = f * imf_plus_primaries(m, self.initial_mass_function)
                    fm12 = fm1 + f * imf_binary_secondary(m, self.initial_mass_function, SNI_events = False)
                    fm2s = f * imf_binary_secondary(m, self.initial_mass_function, SNI_events = True)
                    fmr = f * imf_remnants(m, self.initial_mass_function, self.context["expelled"])
                    fik += fm12
                    if m > constants.MSN2 : fisiik += fm1/m

                    if self.context["sn_ia_selection"] == "matteucci":
                        fisik_a += fm2s/m
                        fisik_b = 0
                    elif self.context["sn_ia_selection"] == "tornambe":
                        fisik_a = vnak
                        fisik_b = vnbk
                    elif self.context["sn_ia_selection"] == "rlp":
                        fisik_a = sn_ratek
                        fisik_b = 0

                    q += fm12 * qm

                    if m < self.bmaxm:
                       q += (fisik_a * q_sn_ia) + (fisik_b * q_sn_ib)



            imf_sn_file.write(f'{fik:.4f}'
                              + f'  {fisiik:.4f}'
                              + f'  {fisik_a:.4f}'
                              + f'  {fisik_b:.4f}'
                              + f'  {vnbk:.4f}'
                              + f'  {etk:.4f}'
                              + '\n'
                             )

            self.write_matrix_file(m_inf, m_sup, q)
        imf_sn_file.close()


    def eta(self):
        # ETA Computation:  Proportion of stars with mass in [bmin, bmax] * alpha_bin_stars
        # In the end ETA is the number of binary systems
        eta = 0.0
        stm = (constants.BMAX - constants.BMIN) / (constants.NW - 1)

        for i in range(0, constants.NW):
            bm = constants.BMIN + i * stm
            eta += self.w[i] * self.initial_mass_function.for_mass(bm) / bm

        return self.context["alpha_bin_stars"] * stm * eta

    def explosive_nucleosynthesis(self):

        mass_intervals_file = open("mass_intervals", "w")
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
            self.vna.append((supernovas_a_rate(t_sup) - supernovas_a_rate(t_inf)) * self.eta)
            self.vnb.append((supernovas_b_rate(t_sup) - supernovas_b_rate(t_inf)) * self.eta)

            self.et.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_rate.append(self.context["alpha_bin_stars"] * 0.5 *
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

            self.vna.append((supernovas_a_rate(t_sup) - supernovas_a_rate(t_inf)) * self.eta)
            self.vnb.append((supernovas_b_rate(t_sup) - supernovas_b_rate(t_inf)) * self.eta)

            self.et.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_rate.append(self.context["alpha_bin_stars"] * 0.5 *
                (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)) * self.delt1)

            ii = constants.LM2 + interval

        mass_intervals_file.close()

    def write_matrix_file(self, m_inf, m_sup, matrix):
        matrix_file = open(f"q-matrices/q_{m_inf}_{m_sup}", "w")
        with np.printoptions(suppress=True, linewidth=500):
            matrix_file.write(str(matrix))
        matrix_file.close()
