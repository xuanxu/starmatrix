import math
import numpy as np
import starmatrix.constants as constants
import starmatrix.elements as elements
import starmatrix.matrix as matrix
from starmatrix.imfs import select_imf
from starmatrix.abundances import select_abundances
from starmatrix.dtds import select_dtd, dtd_correction
from starmatrix.functions import stellar_mass, stellar_lifetime, max_mass_allowed, return_fraction
from starmatrix.functions import total_energy_ejected, newton_cotes, global_imf, imf_supernovae_II


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
        self.integration_step = self.context["integration_step"]
        self.total_time_steps = 0
        if "total_time_steps" in self.context:
            self.total_time_steps = self.context["total_time_steps"]

        self.bmaxm = constants.B_MAX / 2

    def run(self):
        self.explosive_nucleosynthesis()
        self.create_q_matrices()

    def create_q_matrices(self):
        q_sn_ia = matrix.q_sn(constants.CHANDRASEKHAR_LIMIT, feh=self.context["abundances"].feh(), sn_yields=self.context["sn_yields"])
        imf_sn_file = open(f"{self.context['output_dir']}/imf_supernova_rates", "w+")
        matrices_file = open(f"{self.context['output_dir']}/qm-matrices", "w+")
        if self.context["return_fractions"] is True:
            return_fraction_file = open(f"{self.context['output_dir']}/return_fractions", "w+")

        for i in range(0, self.total_time_steps):
            m_inf, m_sup = self.mass_intervals[i]
            q = np.zeros((constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS))
            phi, supernova_Ia_rates, supernova_II_rates, r = 0.0, 0.0, 0.0, 0.0

            if m_sup > constants.M_MIN and m_sup > m_inf:
                q += newton_cotes(
                    m_inf,
                    m_sup,
                    lambda m:
                        global_imf(m, self.initial_mass_function, self.context["binary_fraction"]) *
                        matrix.q(m, self.context)
                )

                supernova_Ia_rates = self.sn_Ia_rates[i] * self.initial_mass_function.stars_per_mass_unit * dtd_correction(self.context)
                q += q_sn_ia * supernova_Ia_rates

                phi = newton_cotes(
                    m_inf,
                    m_sup,
                    lambda m:
                        global_imf(m, self.initial_mass_function, self.context["binary_fraction"])
                )

                supernova_II_rates = newton_cotes(
                    m_inf,
                    m_sup,
                    lambda m:
                        imf_supernovae_II(m, self.initial_mass_function, self.context["binary_fraction"])
                )

                if self.context["return_fractions"] is True:
                    r = return_fraction(m_inf, m_sup, self.context["expelled"], self.initial_mass_function, self.context["binary_fraction"])

            np.savetxt(matrices_file, q, fmt="%15.10f", header=self._matrix_header(m_sup, m_inf))
            imf_sn_file.write(f"  {phi:.10f}  {supernova_Ia_rates:.10f}  {supernova_II_rates:.10f}  {self.energies[i]:.10f}\n")
            if self.context["return_fractions"] is True:
                return_fraction_file.write(f"{r:.10f}\n")

        matrices_file.close()
        imf_sn_file.close()
        if self.context["return_fractions"] is True:
            return_fraction_file.close()

    def explosive_nucleosynthesis(self):
        if self.integration_step == "logt":
            self.explosive_nucleosynthesis_step_logt()
        elif self.integration_step == "t":
            self.explosive_nucleosynthesis_step_t()
        elif self.integration_step == "two_steps_t":
            self.explosive_nucleosynthesis_two_steps_t()
        elif self.integration_step == "fixed_n_steps":
            steps_small_stars = self.context["integration_steps_stars_smaller_than_4Msun"]
            steps_massive_stars = self.context["integration_steps_stars_bigger_than_4Msun"]
            self.explosive_nucleosynthesis_fixed_n_steps(steps_massive_stars, steps_small_stars)
        else:
            raise ValueError("Invalid value for integration step. Should be one of: [logt, t, two_steps_t, fixed_n_steps]")

    def explosive_nucleosynthesis_step_logt(self):
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
            self.sn_Ia_rates.append(newton_cotes(t_inf, t_sup, self.dtd))

        mass_intervals_file.close()

    def explosive_nucleosynthesis_step_t(self):
        t_ini = stellar_lifetime(self.m_max, self.z)
        t_end = min(stellar_lifetime(self.m_min, self.z), constants.TOTAL_TIME)

        delta_t = (t_end - t_ini) / self.total_time_steps

        mass_intervals_file = open(f"{self.context['output_dir']}/mass_intervals", "w+")
        mass_intervals_file.write(" ".join([str(i) for i in [t_ini, t_end, self.total_time_steps, delta_t]]))

        for step in range(0, self.total_time_steps):
            t_inf = t_ini + (delta_t * step)
            t_sup = t_ini + (delta_t * (step + 1))

            m_inf = stellar_mass(t_sup, self.z)
            m_sup = stellar_mass(t_inf, self.z)

            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(step + 1))

            self.mass_intervals.append([m_inf, m_sup])
            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_Ia_rates.append(newton_cotes(t_inf, t_sup, self.dtd))

        mass_intervals_file.close()

    def explosive_nucleosynthesis_two_steps_t(self):
        t_ini = stellar_lifetime(self.m_max, self.z)
        t_limit_massive = stellar_lifetime(4.0, self.z)
        t_end = min(stellar_lifetime(self.m_min, self.z), constants.TOTAL_TIME)

        delta_t_1 = stellar_lifetime(100.0, self.z) / 2
        delta_t_2 = 50 * delta_t_1

        steps_with_delta_t_1 = math.ceil((t_limit_massive - t_ini) / delta_t_1)
        t_ini_for_delta_2 = t_ini + (delta_t_1 * steps_with_delta_t_1)
        steps_with_delta_t_2 = math.ceil((t_end - t_ini_for_delta_2) / delta_t_2)
        delta_t_2 = (t_end - t_ini_for_delta_2) / steps_with_delta_t_2
        self.total_time_steps = steps_with_delta_t_1 + steps_with_delta_t_2

        mass_intervals_file = open(f"{self.context['output_dir']}/mass_intervals", "w+")
        mass_intervals_file.write(" ".join([str(i) for i in [t_ini, t_end, steps_with_delta_t_1, steps_with_delta_t_2, delta_t_1, delta_t_2]]))

        for step in range(0, steps_with_delta_t_1):
            t_inf = t_ini + (delta_t_1 * step)
            t_sup = t_ini + (delta_t_1 * (step + 1))

            m_inf = stellar_mass(t_sup, self.z)
            m_sup = stellar_mass(t_inf, self.z)

            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(step + 1))

            self.mass_intervals.append([m_inf, m_sup])
            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_Ia_rates.append(newton_cotes(t_inf, t_sup, self.dtd))

        for step in range(0, steps_with_delta_t_2):
            t_inf = t_ini_for_delta_2 + (delta_t_2 * step)
            t_sup = t_ini_for_delta_2 + (delta_t_2 * (step + 1))

            m_inf = stellar_mass(t_sup, self.z)
            m_sup = stellar_mass(t_inf, self.z)

            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(step + 1))

            self.mass_intervals.append([m_inf, m_sup])
            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_Ia_rates.append(newton_cotes(t_inf, t_sup, self.dtd))

        mass_intervals_file.close()

    def explosive_nucleosynthesis_fixed_n_steps(self, n_massive, n_small):
        t_ini = stellar_lifetime(self.m_max, self.z)
        t_limit_massive = stellar_lifetime(4.0, self.z)
        t_end = min(stellar_lifetime(self.m_min, self.z), constants.TOTAL_TIME)

        delta_t_1 = (t_limit_massive - t_ini) / n_massive
        delta_t_2 = (t_end - t_limit_massive) / n_small

        self.total_time_steps = n_massive + n_small

        mass_intervals_file = open(f"{self.context['output_dir']}/mass_intervals", "w+")
        mass_intervals_file.write(" ".join([str(i) for i in [t_ini, t_end, n_massive, n_small, delta_t_1, delta_t_2]]))

        for step in range(0, n_massive):
            t_inf = t_ini + (delta_t_1 * step)
            t_sup = t_ini + (delta_t_1 * (step + 1))

            m_inf = stellar_mass(t_sup, self.z)
            m_sup = stellar_mass(t_inf, self.z)

            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(step + 1))

            self.mass_intervals.append([m_inf, m_sup])
            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_Ia_rates.append(newton_cotes(t_inf, t_sup, self.dtd))

        for step in range(0, n_small):
            t_inf = t_limit_massive + (delta_t_2 * step)
            t_sup = t_limit_massive + (delta_t_2 * (step + 1))

            m_inf = stellar_mass(t_sup, self.z)
            m_sup = stellar_mass(t_inf, self.z)

            mass_intervals_file.write('\n' + f'{m_sup:14.10f}  ' + f'{m_inf:14.10f}  ' + str(step + 1))

            self.mass_intervals.append([m_inf, m_sup])
            self.energies.append(total_energy_ejected(t_sup) - total_energy_ejected(t_inf))
            self.sn_Ia_rates.append(newton_cotes(t_inf, t_sup, self.dtd))

        mass_intervals_file.close()

    def _matrix_header(self, m_sup, m_inf):
        if self.context["matrix_headers"] is True:
            return f"Q matrix for mass interval: [{m_sup}, {m_inf}]"
        else:
            return ""
