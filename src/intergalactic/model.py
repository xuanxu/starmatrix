import math
import numpy as np
import intergalactic.constants as constants
import intergalactic.elements as elements
import intergalactic.matrix as matrix
from intergalactic.imfs import select_imf
from intergalactic.abundances import select_abundances
from intergalactic.dtds import select_dtd
from intergalactic.functions import stellar_mass, stellar_lifetime, max_mass_allowed, mass_from_tau
from intergalactic.functions import total_energy_ejected, newton_cotes, global_imf, imf_supernovas_II


class Model:
    def __init__(self, settings={}):
        self.context = settings
        self.init_variables()

    def init_variables(self):
        self.initial_mass_function = select_imf(self.context["imf"], self.context)
        self.context["abundances"] = select_abundances(self.context["sol_ab"], float(self.context["z"]))
        self.context["expelled"] = elements.Expelled(expelled_elements_filename=self.context["expelled_elements_filename"])

        self.mass_intervals = []
        self.energies = []
        self.sn_Ia_rates = []

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
        q_sn_ia = matrix.q_sn(constants.CHANDRASEKHAR_LIMIT, feh=self.context["abundances"].feh(), sn_type="sn_ia")
        imf_sn_file = open(f"{self.context['output_dir']}/imf_supernova_rates", "w+")
        matrices_file = open(f"{self.context['output_dir']}/qm-matrices", "w+")

        for i in range(0, self.total_time_steps):
            m_inf, m_sup = self.mass_intervals[i]
            q = np.zeros((constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS))
            phi, supernova_Ia_rates, supernova_II_rates = 0.0, 0.0, 0.0

            if m_sup > constants.M_MIN and m_sup > m_inf:
                q += newton_cotes(
                    m_inf,
                    m_sup,
                    lambda m:
                        global_imf(m, self.initial_mass_function, self.context["binary_fraction"]) *
                        matrix.q(m, self.context)
                )

                phi = newton_cotes(
                    m_inf,
                    m_sup,
                    lambda m:
                        global_imf(m, self.initial_mass_function, self.context["binary_fraction"])
                )

                if m_inf < self.bmaxm:
                    supernova_Ia_rates = self.sn_Ia_rates[i]
                    q += q_sn_ia * supernova_Ia_rates

                supernova_II_rates = newton_cotes(
                    m_inf,
                    m_sup,
                    lambda m:
                        imf_supernovas_II(m, self.initial_mass_function, self.context["binary_fraction"])
                )

            np.savetxt(matrices_file, q, fmt="%15.10f", header=self._matrix_header(m_sup, m_inf))
            imf_sn_file.write(f"  {phi:.10f}  {supernova_Ia_rates:.10f}  {supernova_II_rates:.10f}  {self.energies[i]:.10f}\n")

        matrices_file.close()
        imf_sn_file.close()

    def explosive_nucleosynthesis(self):

        t_ini = stellar_lifetime(self.m_max, 0.05)
        t_end = constants.TOTAL_TIME

        delta_t = (t_end - t_ini) / self.total_time_steps

        mass_intervals_file = open(f"{self.context['output_dir']}/mass_intervals", "w+")
        mass_intervals_file.write(" ".join([str(i) for i in [t_ini, t_end, self.total_time_steps, delta_t]]))

        for step in range(0, self.total_time_steps):
            t_inf = t_ini + (delta_t * step)
            t_sup = t_ini + (delta_t * (step + 1))

            m_inf = mass_from_tau(t_sup, self.z)
            m_sup = mass_from_tau(t_inf, self.z)

            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(step + 1))

            self.mass_intervals.append([m_inf, m_sup])
            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_Ia_rates.append(self.context["binary_fraction"] * newton_cotes(t_inf, t_sup, self.dtd))

        mass_intervals_file.close()

    def _matrix_header(self, m_sup, m_inf):
        if self.context["matrix_headers"] is True:
            return f"Q matrix for mass interval: [{m_sup}, {m_inf}]"
        else:
            return ""
