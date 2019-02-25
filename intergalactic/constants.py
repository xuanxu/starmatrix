# Q-matrices size:
Q_MATRIX_ROWS = 15
Q_MATRIX_COLUMNS = 9

# Mass range config:
M_MIN = 0.8         # Minimum mass
M_SEP = 4.0         # Limit mass value between small and massive stars

# Binaries params:
M_SNII = 8.0        # Lower limit for binaries in Supernovas II
B_MIN  = 3.0        # Lower limit for binaries in Supernovas I
B_MAX  = 16.0       # Upper limit for binaries in Supernovas I
BIN_FRACTION = 0.05 # Fraction of binaries

# Integration values:
N_POINTS = 7
N_INTERVALS = N_POINTS - 1
IMF_WEIGHTS = [41.0, 216.0, 27.0, 272.0, 27.0, 216.0, 41.0, 0.0, 0.0, 0.0]
WEIGHTS_N = [i * (N_POINTS - 1) / sum(IMF_WEIGHTS) for i in IMF_WEIGHTS]

# Model calculations params:
M_STEP     = 164    # step size for mass intervals of massive stars
LOW_M_STEP = 82     # number of steps for mass intervals of low mass stars
TOTAL_TIME = 13.25  # Total integration time in Gigayears