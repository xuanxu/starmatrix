import math
import numpy as np
import intergalactic.constants as constants
import intergalactic.elements as elements
import intergalactic.matrix as matrix
from intergalactic.functions import select_imf, select_abundances, select_dtd
from intergalactic.functions import stellar_mass, stellar_lifetime, max_mass_allowed
from intergalactic.functions import total_energy_ejected, newton_cotes, global_imf

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

        self.z = self.context["z"]
        self.dtd = select_dtd(self.context["dtd_sn"])
        self.m_min = self.context["m_min"]
        self.m_max = self.context["m_max"]
        self.total_time_steps = self.context["total_time_steps"]

        self.bmaxm = constants.B_MAX / 2

    def run(self):
        self.explosive_nucleosynthesis()
        self.create_q_matrices()

    def create_q_matrices(self):
        q_sn_ia = matrix.q_sn(constants.CHANDRASEKHAR_LIMIT, self.context["abundances"].feh(), sn_type = "sn_ia")
        imf_sn_file = open(f"{self.context['output_dir']}/imf_supernova_rates", "w+")
        matrices_file =  open(f"{self.context['output_dir']}/qm-matrices", "w+")

        q = np.zeros((constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS))
        for i in range(0, self.total_time_steps):
            m_inf, m_sup = self.mass_intervals[i]
            supernova_rates = 0.0

            if m_sup <= constants.M_MIN or m_sup <= m_inf : continue

            q += newton_cotes(m_inf, m_sup, lambda m : \
                    global_imf(m, self.initial_mass_function, self.context["binary_fraction"]) * \
                    matrix.q(m, self.context))

            if m_inf < self.bmaxm:
                supernova_rates = self.sn_rates[i]
                q += q_sn_ia * supernova_rates


            np.savetxt(matrices_file, q, fmt="%15.10f", header=f"Q matrix for mass interval: [{m_sup}, {m_inf}]")
            imf_sn_file.write(f"  {supernova_rates:.10f}  {self.energies[i]:.10f}\n")

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
            self.sn_rates.append(self.context["binary_fraction"] * newton_cotes(t_inf, t_sup, self.dtd))

        mass_intervals_file.close()
