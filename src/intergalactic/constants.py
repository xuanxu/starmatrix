# Q-matrices size:
Q_MATRIX_ROWS = 15
Q_MATRIX_COLUMNS = 9

# Mass range config:
M_MIN = 0.8         # Minimum mass
CHANDRASEKHAR_LIMIT = 1.4

# Binaries params:
M_SNII = 8.0        # Lower limit for binaries in Supernovas II
B_MIN  = 3.0        # Lower limit for binaries in Supernovas I
B_MAX  = 16.0       # Upper limit for binaries in Supernovas I
BIN_FRACTION = 0.05 # Fraction of binaries

# Values for integration using Newton-Cotes formula:
NEWTON_COTES_POINTS = 7
NEWTON_COTES_INTERVALS = 6
NEWTON_COTES_COEFFICIENTS = [0.29285714, 1.54285714, 0.19285714, 1.94285714, 0.19285714, 1.54285714, 0.29285714]

# Model calculations params:
TOTAL_TIME = 13.25  # Total integration time in Gigayears