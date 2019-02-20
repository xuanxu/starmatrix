Q_MATRIX_ROWS = 15
Q_MATRIX_COLUMNS = 9
NW = 7
IMF_WEIGHTS = [41.0, 216.0, 27.0, 272.0, 27.0, 216.0, 41.0, 0.0, 0.0, 0.0]
W_NW = [i * (NW - 1) / sum(IMF_WEIGHTS) for i in IMF_WEIGHTS]
MMIN = 0.8

# FROM PARGRA
IC = 1
LM2 = 164
LBLK = 82
MSEP = 4.0    # Limit mass value between small and massive stars
MSN2 = 8.0    # Lower limit for binaries in Supernovas II
BMIN = 3.0    # Lower limit for binaries in Supernovas I
BMAX = 16.0   # Upper limit for binaries in Supernovas I
ALF = 0.05    # Fraction of binaries
TTOT = 13.25  # Total integration time in Gigayears
