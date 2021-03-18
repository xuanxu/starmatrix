
"""
Datasets of Supernova ejections for different metallicities

"""

sn_elements_list = ["He4", "C12", "C13", "N14", "O16", "Ne", "Mg", "Si", "S", "Ca", "Fe"]


def empty_yields_set():
    return dict(zip(sn_elements_list, [0.0 for i in range(11)]))


def yields(dataset_key, feh):
    datasets = {
        "iwa1998": yields_from_iwamoto,
        "sei2013": yields_from_seitenzahl
    }
    sn_yields = datasets[dataset_key](feh)
    return dict(zip(sn_elements_list, sn_yields))


def yields_from_iwamoto(feh):
    """
    Supernova data source: Iwamoto, K. et al., 1999, ApJ 125, 439
    """
    if feh < -0.3:
        return [0.0, 0.0508, 1.56e-9, 3.31e-8, 0.133, 0.00229, 0.0158, 0.142, 0.0914, 0.0181, 0.68]
    else:
        return [0.0, 0.0483, 1.40e-6, 1.16e-6, 0.143, 0.00202, 0.0085, 0.154, 0.0846, 0.0119, 0.626]


def yields_from_seitenzahl(feh):
    """
    Supernova data source: Seitenzahl et al. 2013, MNRAS, Vol 429, Issue 2, 1156–1172
    The four datasets are provided for FeH values of -2, -1, -0.301 and 0. We assign them to 4 intervals.
    """
    if feh <= -1.5:
        return [0.0, 3.16e-03, 2.72e-10, 7.22e-08, 9.47e-02, 3.74e-03, 2.90e-02, 2.89e-01, 1.15e-01, 1.77e-02, 6.72e-01]
    elif -1.5 < feh <= -0.65:
        return [0.0, 3.15e-03, 1.91e-09, 4.71e-07, 9.64e-02, 3.69e-03, 2.69e-02, 2.94e-01, 1.12e-01, 1.66e-02, 6.66e-01]
    elif -0.65 < feh <= -0.15:
        return [0.0, 3.10e-03, 8.47e-09, 1.80e-06, 9.87e-02, 3.06e-03, 2.02e-02, 2.90e-01, 1.12e-01, 1.57e-02, 6.46e-01]
    elif -0.15 < feh:
        return [0.0, 3.04e-03, 1.74e-08, 3.21e-06, 1.01e-01, 3.53e-03, 1.52e-02, 2.84e-01, 1.11e-01, 1.47e-02, 6.22e-01]
