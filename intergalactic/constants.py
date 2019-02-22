# Q-matrices size:
Q_MATRIX_ROWS = 15
Q_MATRIX_COLUMNS = 9

# Integration Values:
N_POINTS = 7
N_INTERVALS = N_POINTS - 1
IMF_WEIGHTS = [41.0, 216.0, 27.0, 272.0, 27.0, 216.0, 41.0, 0.0, 0.0, 0.0]
WEIGHTS_N = [i * (N_POINTS - 1) / sum(IMF_WEIGHTS) for i in IMF_WEIGHTS]

# Mass range config:
MMIN = 0.8    # Minimum mass
MSEP = 4.0    # Limit mass value between small and massive stars

# Binaries params:
MSN2 = 8.0    # Lower limit for binaries in Supernovas II
BMIN = 3.0    # Lower limit for binaries in Supernovas I
BMAX = 16.0   # Upper limit for binaries in Supernovas I
BIN_FRACTION  = 0.05   # Fraction of binaries

# Model params:
LM2 = 164
LBLK = 82
TOTAL_TIME = 13.25  # Total integration time in Gigayears