import numpy as np
import intergalactic.constants as constants
import intergalactic.elements as elements
import intergalactic.matrix as matrix
from intergalactic.functions import select_imf, select_abundances
from intergalactic.functions import mean_lifetime, stellar_mass
from intergalactic.functions import total_energy_ejected, sn_rate_ruiz_lapuente, value_in_interval
from intergalactic.functions import imf_plus_primaries, imf_binary_secondary, imf_remnants

class Model:
    def __init__(self, settings = {}):
        self.context = settings
        self.init_variables()

    def init_variables(self):
        self.initial_mass_function = select_imf(self.context["imf"], self.context)
        self.context["abundances"] = select_abundances(self.context["sol_ab"], float(self.context["z"]))
        self.context["expelled"] = elements.Expelled(expelled_elements_filename=self.context["expelled_elements_filename"])

        self.mass_intervals = []
        self.energies = []
        self.sn_rates = []

        tsep         = mean_lifetime(constants.M_SEP, 0.02)
        self.delta   = tsep / constants.M_STEP
        self.delta_low_m   = constants.LOW_M_STEP * self.delta
        self.lm1     = int(1 + (constants.M_STEP * constants.TOTAL_TIME) / (tsep * constants.LOW_M_STEP))
        self.bmaxm   = constants.B_MAX / 2

    def run(self):

        self.eta = self.eta()
        self.explosive_nucleosynthesis()
        self.create_q_matrices()

    def create_q_matrices(self):
        # Chandrasekhar limit = 1.4
        feh = self.context["abundances"].feh()
        q_sn_ia = matrix.q_sn(1.4, feh, sn_type = "sn_ia")[0:constants.Q_MATRIX_ROWS, 0:constants.Q_MATRIX_COLUMNS]

        imf_sn_file = open(f"{self.context['output_dir']}/imf_supernova_rates", "w+")
        matrices_file =  open(f"{self.context['output_dir']}/qm-matrices", "w+")

        for i in range(0, constants.M_STEP + self.lm1):
            m_inf, m_sup = self.mass_intervals[i]
            mass_step = (m_sup - m_inf) / constants.N_INTERVALS

            q = np.zeros((constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS))

            fik, fisik_a, fisiik = 0.0, 0.0, 0.0
            energies_k  = 1e6 * self.energies[i]
            sn_rates_k = 1e6 * self.sn_rates[i]

            if m_sup > constants.M_MIN and mass_step != 0:

                for ip in range(0, constants.N_POINTS):
                    m = m_inf +(mass_step * ip)
                    qm = matrix.q(m, self.context)[0:constants.Q_MATRIX_ROWS, 0:constants.Q_MATRIX_COLUMNS]

                    # Initial mass functions:
                    f = 1e6 * constants.WEIGHTS_N[ip] * mass_step
                    fm1 = f * imf_plus_primaries(m, self.initial_mass_function, self.context["binary_fraction"])
                    fm12 = fm1 + f * imf_binary_secondary(m, self.initial_mass_function, SNI_events = False, binary_fraction=self.context["binary_fraction"])
                    # fmr = f * imf_remnants(m, self.initial_mass_function, self.context["expelled"], binary_fraction=self.context["binary_fraction"])
                    fik += fm12
                    if m > constants.M_SNII : fisiik += fm1/m

                    if self.context["sn_ia_selection"] == "rlp":
                        fisik_a = sn_rates_k

                    q += fm12 * qm

                    if m < self.bmaxm:
                       q += (fisik_a * q_sn_ia)

            np.savetxt(matrices_file, q, fmt="%15.8f", header=f"Q matrix for mass interval: [{m_sup}, {m_inf}]")
            imf_sn_file.write(f'{fik:.4f}'
                              + f'  {fisiik:.4f}'
                              + f'  {fisik_a:.4f}'
                              + f'  {energies_k:.4f}'
                              + '\n'
                             )

        matrices_file.close()
        imf_sn_file.close()

    def eta(self):
        # ETA Computation:  Proportion of stars with mass in [bmin, bmax] * binary_fraction
        # In the end ETA is the number of binary systems
        eta = 0.0
        stm = (constants.B_MAX - constants.B_MIN) / constants.N_INTERVALS

        for i in range(0, constants.N_POINTS):
            bm = constants.B_MIN + i * stm
            eta += constants.WEIGHTS_N[i] * self.initial_mass_function.for_mass(bm) / bm

        return self.context["binary_fraction"] * stm * eta

    def explosive_nucleosynthesis(self):

        mass_intervals_file = open(f"{self.context['output_dir']}/mass_intervals", "w+")
        line_1 = " ".join([str(i) for i in [constants.M_STEP, constants.LOW_M_STEP, self.lm1]])
        line_2 = " ".join([str(i) for i in [self.delta, self.lm1*self.delta_low_m]])
        mass_intervals_file.write("\n".join([line_1, line_2]))

        m_inf = self.context["m_max"]
        t_sup = mean_lifetime(self.context["m_max"], self.context["z"])

        for interval in range(1, constants.M_STEP + 1):
            m_sup = m_inf
            m_inf = stellar_mass(self.delta * interval, self.context["z"])
            m_inf = value_in_interval(m_inf, [constants.M_SEP, self.context["m_max"]])
            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(interval))
            self.mass_intervals.append([m_inf, m_sup])

            t_inf = t_sup
            t_sup = self.delta * interval

            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_rates.append(self.context["binary_fraction"] * 0.5 *
                (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)) * self.delta)


        m_inf = constants.M_SEP
        for interval in range(1, self.lm1 + 1):
            m_sup = m_inf
            m_inf = stellar_mass(self.delta_low_m * interval, self.context["z"])
            if m_inf >= constants.M_SEP : m_inf = m_sup
            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(interval))
            self.mass_intervals.append([m_inf, m_sup])

            t_inf = t_sup
            t_sup = self.delta_low_m * interval
            if t_sup <= t_inf : t_sup = t_inf

            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_rates.append(self.context["binary_fraction"] * 0.5 *
                (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)) * self.delta_low_m)



        mass_intervals_file.close()
