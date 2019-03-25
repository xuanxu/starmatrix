import math
import numpy as np
import intergalactic.constants as constants
import intergalactic.elements as elements
import intergalactic.matrix as matrix
from intergalactic.functions import select_imf, select_abundances
from intergalactic.functions import stellar_mass, stellar_lifetime, max_mass_allowed
from intergalactic.functions import total_energy_ejected, sn_rate_ruiz_lapuente, value_in_interval
from intergalactic.functions import imf_plus_primaries, imf_binary_secondary

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

        self.m_min = self.context["m_min"]
        self.m_max = self.context["m_max"]
        self.z = self.context["z"]
        self.total_time_steps = 300


        tsep         = mean_lifetime(constants.M_SEP, 0.02)
        self.delta   = tsep / constants.M_STEP
        self.delta_low_m   = constants.LOW_M_STEP * self.delta
        self.lm1     = int(1 + (constants.M_STEP * constants.TOTAL_TIME) / (tsep * constants.LOW_M_STEP))
        self.bmaxm   = constants.B_MAX / 2

    def run(self):
        self.explosive_nucleosynthesis()
        self.create_q_matrices()

    def create_q_matrices(self):
        # Chandrasekhar limit = 1.4
        feh = self.context["abundances"].feh()
        q_sn_ia = matrix.q_sn(1.4, feh, sn_type = "sn_ia")[0:constants.Q_MATRIX_ROWS, 0:constants.Q_MATRIX_COLUMNS]

        imf_sn_file = open(f"{self.context['output_dir']}/imf_supernova_rates", "w+")
        matrices_file =  open(f"{self.context['output_dir']}/qm-matrices", "w+")

        for i in range(0, self.total_time_steps):
            m_inf, m_sup = self.mass_intervals[i]
            mass_step = (m_sup - m_inf) / constants.N_INTERVALS

            q = np.zeros((constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS))

            fisik_a = 0.0
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

                    if self.context["sn_ia_selection"] == "rlp":
                        fisik_a = sn_rates_k

                    q += fm12 * qm

                    if m < self.bmaxm:
                       q += (fisik_a * q_sn_ia)

            np.savetxt(matrices_file, q, fmt="%15.8f", header=f"Q matrix for mass interval: [{m_sup}, {m_inf}]")
            imf_sn_file.write(f'  {fisik_a:.4f}'
                              + f'  {energies_k:.4f}'
                              + '\n'
                             )

        matrices_file.close()
        imf_sn_file.close()

    def explosive_nucleosynthesis(self):

        t_ini = stellar_lifetime(min(self.m_max, max_mass_allowed(self.z)), self.z)
        t_end = min(stellar_lifetime(self.m_min, self.z), constants.TOTAL_TIME)
        t_ini_log = math.log10(t_ini * 1e9)
        t_end_log = math.log10(t_end * 1e9)

        delta_t_log = (t_end_log - t_ini_log) / self.total_time_steps

        mass_intervals_file = open(f"{self.context['output_dir']}/mass_intervals", "w+")
        mass_intervals_file.write(" ".join([str(i) for i in [t_ini, t_end, self.total_time_steps, delta_t_log]]))

        for step in range(0, self.total_time_steps):
            t_inf_log = t_ini_log + (delta_t_log * step)
            t_sup_log = t_ini_log + (delta_t_log * (step + 1))

            t_inf = math.pow(10, t_inf_log - 9)
            t_sup = math.pow(10, t_sup_log - 9)

            m_inf = stellar_mass(t_sup, self.z)
            m_sup = stellar_mass(t_inf, self.z)

            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(step + 1))

            self.mass_intervals.append([m_inf, m_sup])
            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_rates.append(self.context["binary_fraction"] * 0.5 * (t_sup - t_inf) * (sn_rate_ruiz_lapuente(t_sup) + sn_rate_ruiz_lapuente(t_inf)))

        mass_intervals_file.close()
