from bisect import bisect
import numpy as np
from scipy.interpolate import interp1d


class Expelled:

    elements_list = ["H", "D", "He3", "He4", "C12", "C13",
                     "N14p", "n.r.", "O16", "Ne", "Mg", "Si",
                     "S", "Ca", "Fe", "remnants", "C13s", "N14s"]
    mass_points = []
    by_mass = {}

    def __init__(self, expelled_elements_filename="expelled_elements"):
        self.mass_points = []
        self.data_rows = []
        self.by_mass = {}
        self.interpolation_function = None
        self.read_expelled_elements_file(expelled_elements_filename)

    def read_expelled_elements_file(self, filename):
        """
        Reads a file of expelled elements per stellar mass.
        The file should include a row of data for each stellar mass.
        Structure of each row should be:
            - First column: stellar mass
            - 2nd to 19th columns: expelled mass of element i
                where i is in this ordered list:
                ["H", "D", "He3", "He4", "C12", "C13",
                 "N14primary", "n.r.", "O16", "Ne", "Mg", "Si",
                 "S", "Ca", "Fe", "remnants", "C13secondary", "N14secondary"]

        """

        expelled_data = open(filename, "r")

        for line in expelled_data:
            data_row = [max(0.0, float(data)) for data in line.split()]
            if data_row:
                mass = data_row.pop(0)  # the first column is the mass
                self.mass_points.append(mass)
                self.data_rows.append(data_row)
                self.by_mass[mass] = dict(zip(self.elements_list, data_row))

        expelled_data.close()
        self.interpolation_function = interp1d(
            np.array(self.mass_points),
            np.matrix.transpose(np.array(self.data_rows)),
            fill_value="extrapolate")

    def for_mass(self, m):
        """
        Interpolates expelled mass (per solar mass) for all elements for a given
        stellar mass, using the data from the class' expelled_elements input file.

        """
        return dict(zip(self.elements_list, self.interpolation_function(m) / m))
