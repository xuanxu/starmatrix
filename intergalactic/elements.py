from bisect import bisect

class Expelled:

    element_list = ["h", "d", "he3", "he4", "c12", "o16", "n14p", "c13", "n.r.", "ne", "mg", "si", "s", "ca", "fe", "remnants", "c13s", "n14s"]
    mass_points = []
    by_mass = {}

    def __init__(self, expelled_elements_filename):
        self.read_expelled_elements_file(expelled_elements_filename)

    def read_expelled_elements_file(self, filename):
        expelled_data = open(filename, "r")

        for line in expelled_data:
            data_row = [max(0.0, float(data)) for data in line.split()]
            mass = data_row.pop(0) # the first column is the mass
            self.mass_points.append(mass)
            self.by_mass[mass] = dict(zip(self.element_list, data_row))

        expelled_data.close()

    def for_mass(self, m):
        if m in self.mass_points : return self.by_mass[m]

        index = bisect(self.mass_points, m)
        mass_prev = self.mass_points[index - 1]
        mass_next = self.mass_points[index]
        elements_prev = self.by_mass[mass_prev]
        elements_next = self.by_mass[mass_next]

        interpolations = {"mass": m}
        p = (mass_next - m) / (mass_next - mass_prev)
        for element  in self.element_list:
            d = elements_next[element] - elements_prev[element]
            interpolations[element] = (elements_next[element] - (p * d) ) / m

        return interpolations
