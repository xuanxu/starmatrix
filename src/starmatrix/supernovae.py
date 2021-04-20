
"""
Datasets of Supernova ejections for different metallicities

"""

sn_elements_list = ["He4", "C12", "C13", "N14", "O16", "Ne", "Mg", "Si", "S", "Ca", "Fe"]


def empty_yields_set():
    return dict(zip(sn_elements_list, [0.0 for i in range(11)]))


def yields(dataset_key, feh):
    datasets = {
        "iwa1998": yields_from_iwamoto,
        "sei2013": yields_from_seitenzahl,
        "ln2018-1": yields_from_leung_nomoto_2018_table6,
        "ln2018-2": yields_from_leung_nomoto_2018_table8,
        "ln2018-3": yields_from_leung_nomoto_2018_table10,
        "ln2020": yields_from_leung_nomoto_2020,
        "br2019-1": yields_from_bravo_2019_table3,
        "br2019-2": yields_from_bravo_2019_table4,
        "gro2021-1": yields_from_gronow_2021_table3_he,
        "gro2021-2": yields_from_gronow_2021_table3_core,
        "mor2018-1": yields_from_mori_2018_w7,
        "mor2018-2": yields_from_mori_2018_wdd2
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


def yields_from_leung_nomoto_2018_table6(feh):
    """
    Supernova data source: Leung & Nomoto, 2018, ApJ, Volume 861, Issue 2, Id 143, Table 6/7
    The seven datasets are provided for Z/Zsun values of 0, 0.1, 0.5, 1, 2, 3 and 5.
    Using Zsun = 0.0169 the corresponding FeH values are -1, -0.301, 0.0, 0.301, 0.4771 and 0.69897.
    We use seven intervals delimited by midpoints of those values.
    """
    if feh <= -1.65:
        return [0.0, 1.58e-3, 7.17e-12, 2.30e-9, 4.19e-2, 2.18e-4, 2.94e-3, 1.62e-1, 1.11e-1, 2.64e-2, 8.46e-1]
    elif -1.65 < feh <= -0.65:
        return [0.0, 1.58e-3, 2.50e-12, 2.74e-10, 4.45e-2, 2.18e-4, 2.61e-3, 1.69e-1, 1.90e-1, 2.38e-2, 8.39e-1]
    elif -0.65 < feh <= -0.15:
        return [0.0, 1.32e-3, 3.79e-12, 3.34e-10, 5.38e-2, 5.48e-4, 2.34e-3, 2.16e-1, 1.25e-1, 2.21e-2, 7.51e-1]
    elif -0.15 < feh <= 0.15:
        return [0.0, 1.31e-3, 8.17e-12, 5.55e-10, 5.45e-2, 5.51e-4, 1.70e-3, 2.20e-1, 1.20e-1, 1.96e-2, 7.25e-1]
    elif 0.15 < feh <= 0.39:
        return [0.0, 1.29e-3, 2.44e-11, 1.13e-9, 5.49e-2, 5.51e-4, 1.15e-3, 2.23e-1, 1.90e-1, 1.62e-2, 6.80e-1]
    elif 0.39 < feh <= 0.59:
        return [0.0, 1.48e-3, 9.60e-12, 2.32e-10, 5.49e-2, 1.69e-4, 8.69e-4, 2.18e-1, 9.92e-2, 1.48e-2, 6.41e-1]
    elif 0.59 <= feh:
        return [0.0, 1.45e-3, 5.68e-11, 6.52e-10, 6.55e-2, 4.36e-4, 1.70e-3, 2.52e-1, 9.45e-2, 1.16e-2, 5.50e-1]


def yields_from_leung_nomoto_2018_table8(feh):
    """
    Supernova data source: Leung & Nomoto, 2018, ApJ, Volume 861, Issue 2, Id 143, Table 8/9
    The seven datasets are provided for Z/Zsun values of 0, 0.1, 0.5, 1, 2, 3 and 5.
    Using Zsun = 0.0169 the corresponding FeH values are -1, -0.301, 0.0, 0.301, 0.4771 and 0.69897.
    We use seven intervals delimited by midpoints of those values.
    """
    if feh <= -1.65:
        return [0.0, 5.93e-4, 1.11e-11, 5.20e-9, 4.22e-2, 6.32e-4, 2.62e-3, 2.40e-1, 1.32e-1, 2.79e-2, 7.40e-1]
    elif -1.65 < feh <= -0.65:
        return [0.0, 5.89e-4, 2.56e-12, 5.60e-10, 4.64e-2, 6.36e-4, 2.30e-3, 2.13e-1, 1.29e-1, 2.43e-2, 7.32e-1]
    elif -0.65 < feh <= -0.15:
        return [0.0, 1.80e-3, 1.91e-12, 1.70e-10, 5.62e-2, 1.40e-4, 1.56e-3, 2.30e-1, 1.28e-1, 2.50e-2, 6.94e-1]
    elif -0.15 < feh <= 0.15:
        return [0.0, 1.70e-3, 2.54e-12, 1.40e-10, 5.69e-2, 1.38e-4, 1.10e-3, 2.35e-1, 1.23e-1, 1.79e-2, 6.71e-1]
    elif 0.15 < feh <= 0.39:
        return [0.0, 1.50e-3, 4.48e-12, 1.39e-10, 5.73e-2, 1.33e-4, 7.39e-4, 2.39e-1, 1.11e-1, 1.44e-2, 6.32e-1]
    elif 0.39 < feh <= 0.59:
        return [0.0, 1.40e-3, 2.65e-11, 4.20e-10, 6.62e-2, 6.78e-4, 1.00e-3, 2.31e-1, 9.59e-2, 1.19e-2, 5.98e-1]
    elif 0.59 <= feh:
        return [0.0, 1.30e-3, 1.37e-10, 6.32e-10, 7.26e-2, 4.18e-4, 9.25e-4, 2.47e-1, 8.98e-2, 1.10e-2, 4.92e-1]


def yields_from_leung_nomoto_2018_table10(feh):
    """
    Supernova data source: Leung & Nomoto, 2018, ApJ, Volume 861, Issue 2, Id 143, Table 10/11
    The seven datasets are provided for Z/Zsun values of 0, 0.1, 0.5, 1, 2, 3 and 5.
    Using Zsun = 0.0169 the corresponding FeH values are -1, -0.301, 0.0, 0.301, 0.4771 and 0.69897.
    We use seven intervals delimited by midpoints of those values.
    """
    if feh <= -1.65:
        return [0.0, 5.48e-4, 1.3e-11, 2.15e-9, 3.46e-2, 1.63e-4, 2.50e-3, 1.72e-1, 1.14e-1, 2.55e-2, 7.57e-1]
    elif -1.65 < feh <= -0.65:
        return [0.0, 5.44e-4, 1.54e-12, 4.34e-10, 3.81e-2, 1.63e-4, 1.84e-3, 1.79e-1, 1.12e-1, 2.24e-2, 7.60e-1]
    elif -0.65 < feh <= -0.15:
        return [0.0, 5.88e-4, 3.24e-12, 2.94e-10, 4.85e-2, 6.58e-4, 1.69e-3, 2.30e-1, 1.14e-1, 1.84e-2, 7.20e-1]
    elif -0.15 < feh <= 0.15:
        return [0.0, 5.82e-4, 6.45e-12, 3.69e-10, 4.90e-2, 6.56e-4, 1.22e-3, 2.8e-1, 1.9e-1, 1.59e-2, 6.81e-1]
    elif 0.15 < feh <= 0.39:
        return [0.0, 5.71e-4, 1.62e-11, 5.52e-10, 4.94e-2, 6.46e-4, 8.41e-4, 2.13e-1, 9.81e-2, 1.26e-2, 6.44e-1]
    elif 0.39 < feh <= 0.59:
        return [0.0, 5.47e-4, 5.54e-11, 9.20e-10, 6.23e-2, 6.82e-4, 7.57e-4, 2.21e-1, 9.27e-2, 1.11e-2, 5.87e-1]
    elif 0.59 <= feh:
        return [0.0, 5.36e-4, 8.29e-11, 7.60e-10, 7.54e-2, 2.81e-4, 8.39e-4, 2.25e-1, 8.00e-2, 8.93e-3, 4.99e-1]


def yields_from_leung_nomoto_2020(feh):
    """
    Supernova data source: Leung & Nomoto, 2020, ApJ, Vol 888, Issue 2, Id 80
    The seven datasets are provided for Z/Zsun values of 0, 0.1, 0.5, 1, 2, 3 and 5.
    Using Zsun = 0.0169 the corresponding FeH values are -1, -0.301, 0.0, 0.301, 0.4771 and 0.69897.
    We use seven intervals delimited by midpoints of those values.
    """
    if feh <= -1.65:
        return [0.0, 3.39e-3, 3.33e-10, 1.16e-8, 1.14e-1, 3.98e-3, 1.70e-2, 1.17e-1, 5.40e-2, 1.11e-2, 6.73e-1]
    elif -1.65 < feh <= -0.65:
        return [0.0, 3.38e-3, 1.22e-10, 4.53e-9, 1.14e-1, 3.96e-3, 1.60e-2, 1.22e-1, 5.28e-2, 9.73e-3, 6.69e-1]
    elif -0.65 < feh <= -0.15:
        return [0.0, 3.38e-3, 3.41e-10, 1.37e-8, 1.16e-1, 4.40e-3, 1.11e-2, 1.36e-1, 6.14e-2, 9.38e-3, 6.34e-1]
    elif -0.15 < feh <= 0.15:
        return [0.0, 3.35e-3, 1.25e-9, 3.80e-8, 1.17e-1, 4.00e-3, 8.26e-3, 1.35e-1, 6.80e-2, 8.49e-3, 6.10e-1]
    elif 0.15 < feh <= 0.39:
        return [0.0, 3.29e-3, 4.59e-9, 9.63e-8, 1.19e-1, 3.86e-3, 5.46e-3, 1.32e-1, 5.69e-2, 7.14e-3, 5.83e-1]
    elif 0.39 < feh <= 0.59:
        return [0.0, 2.62e-3, 2.90e-8, 6.40e-7, 1.12e-1, 3.42e-3, 3.77e-3, 1.30e-1, 5.33e-2, 6.79e-3, 5.57e-1]
    elif 0.59 <= feh:
        return [0.0, 2.20e-3, 1.20e-8, 9.43e-8, 1.40e-1, 3.16e-3, 2.66e-3, 1.40e-1, 3.91e-2, 5.45e-3, 5.15e-1]


def yields_from_bravo_2019_table3(feh):
    """
    Supernova data source: Bravo, E., Badenes, C., Martínez-Rodríguez, H., 2019, MNRAS, Vol 482, Issue 4, 4346–4363, Table 3
    Five datasets are provided for FeH values of -2, -1 -0.4, 0 and 0.5.
    We use five intervals delimited by midpoints of those values.
    """
    if feh <= -1.5:
        return [1.09e-03, 1.24e-03, 7.75e-11, 1.14e-05, 6.54e-02, 6.75e-04, 1.06e-02, 1.95e-01, 1.38e-01, 4.54e-02, 8.25e-01]
    elif -1.5 < feh <= -0.7:
        return [1.23e-03, 1.23e-03, 1.09e-09, 8.94e-06, 6.67e-02, 6.67e-04, 9.33e-03, 2.00e-01, 1.38e-01, 4.23e-02, 8.22e-01]
    elif -0.7 < feh <= -0.2:
        return [2.62e-04, 1.28e-03, 4.42e-09, 6.09e-06, 7.15e-02, 7.06e-04, 7.26e-03, 2.10e-01, 1.42e-01, 3.98e-02, 8.00e-01]
    elif -0.2 < feh <= 0.25:
        return [7.43e-04, 1.27e-03, 1.07e-08, 3.57e-06, 7.25e-02, 7.10e-04, 4.96e-03, 2.12e-01, 1.40e-01, 3.48e-02, 7.90e-01]
    elif 0.25 <= feh:
        return [8.03e-05, 1.28e-03, 2.75e-08, 1.34e-06, 7.48e-02, 7.70e-04, 2.80e-03, 2.10e-01, 1.23e-01, 2.39e-02, 7.75e-01]


def yields_from_bravo_2019_table4(feh):
    """
    Supernova data source: Bravo, E., Badenes, C., Martínez-Rodríguez, H., 2019, MNRAS, Vol 482, Issue 4, 4346–4363, Table 4
    Five datasets are provided for FeH values of -2, -1 -0.4, 0 and 0.5.
    We use five intervals delimited by midpoints of those values.
    """
    if feh <= -1.5:
        return [5.13e-03, 7.27e-04, 4.53e-11, 7.91e-06, 3.57e-02, 2.91e-04, 4.28e-03, 1.31e-01, 9.60e-02, 3.11e-02, 7.11e-01]
    elif -1.5 < feh <= -0.7:
        return [5.12e-03, 7.26e-04, 6.64e-10, 6.17e-06, 3.69e-02, 2.88e-04, 3.75e-03, 1.35e-01, 9.59e-02, 2.89e-02, 7.08e-01]
    elif -0.7 < feh <= -0.2:
        return [4.90e-03, 7.07e-04, 2.73e-09, 4.02e-06, 3.75e-02, 2.80e-04, 2.61e-03, 1.38e-01, 9.62e-02, 2.63e-02, 7.01e-01]
    elif -0.2 < feh <= 0.25:
        return [4.42e-03, 6.75e-04, 6.32e-09, 2.19e-06, 3.75e-02, 2.69e-04, 1.66e-03, 1.38e-01, 9.35e-02, 2.29e-02, 6.91e-01]
    elif 0.25 <= feh:
        return [2.84e-03, 5.86e-04, 1.38e-08, 6.03e-07, 3.41e-02, 2.48e-04, 7.78e-04, 1.30e-01, 7.73e-02, 1.51e-02, 6.70e-01]


def yields_from_gronow_2021_table3_he(feh):
    """
    Supernova data source: Gronow, S. et al., 2021, A&A, Table 3/A10 He detonation
    Five datasets are provided for FeH values of -2, -1, 0 and 0.4771
    We use four intervals delimited by midpoints of those values.
    """
    if feh <= -1.5:
        return [2.10e-2, 7.39e-6, 4.23e-9, 1.25e-7, 3.02e-3, 1.77e-6, 2.29e-4, 3.69e-2, 1.61e-2, 3.70e-3, 4.47e-2]
    elif -1.5 < feh <= -0.5:
        return [2.10e-2, 7.25e-6, 4.21e-9, 1.16e-6, 3.02e-3, 2.03e-6, 2.34e-4, 3.69e-2, 1.61e-2, 3.70e-3, 4.47e-2]
    elif -0.5 < feh <= 0.239:
        return [2.10e-2, 1.09e-5, 3.87e-9, 1.71e-5, 3.09e-3, 7.97e-6, 2.53e-4, 3.71e-2, 1.61e-2, 3.70e-3, 4.48e-2]
    elif 0.239 <= feh:
        return [2.00e-2, 7.52e-6, 3.65e-9, 3.46e-5, 3.24e-3, 1.06e-5, 2.56e-4, 3.76e-2, 1.63e-2, 3.76e-3, 4.45e-2]


def yields_from_gronow_2021_table3_core(feh):
    """
    Supernova data source: Gronow, S. et al., 2021, A&A, Table 3/A10 Core detonation
    Five datasets are provided for FeH values of -2, -1, 0 and 0.4771
    We use four intervals delimited by midpoints of those values.
    """
    if feh <= -1.5:
        return [7.10e-03, 2.46e-06, 2.49e-12, 5.16e-12, 2.70e-03, 1.05e-07, 1.02e-04, 7.28e-02, 5.56e-02, 1.42e-02, 7.98e-01]
    elif -1.5 < feh <= -0.5:
        return [7.10e-03, 2.47e-06, 2.57e-12, 5.26e-12, 2.70e-03, 1.03e-07, 1.06e-04, 7.28e-02, 5.57e-02, 1.42e-02, 7.97e-01]
    elif -0.5 < feh <= 0.239:
        return [6.50e-03, 1.23e-03, 1.95e-09, 1.79e-07, 4.88e-02, 1.78e-03, 3.05e-03, 1.52e-01, 9.29e-02, 1.63e-02, 6.58e-01]
    elif 0.239 <= feh:
        return [4.50e-03, 1.12e-06, 1.12e-12, 6.24e-11, 2.75e-03, 1.16e-07, 4.12e-05, 7.30e-02, 4.89e-02, 1.14e-02, 8.07e-01]


def yields_from_mori_2018_w7(feh):
    """
    Supernova data source: Mori, K. et al., 2018, The Astrophysical Journal, 863:176 W7
    """
    return [0.0, 4.794e-2, 4.150e-8, 5.809e-6, 1.356e-1, 1.309e-3, 1.026e-2, 1.732e-1, 7.890e-2, 1.133e-2, 6.683e-1]


def yields_from_mori_2018_wdd2(feh):
    """
    Supernova data source: Mori, K. et al., 2018, The Astrophysical Journal, 863:176 WDD2
    """
    return [0.0, 1.359e-3, 3.292e-8, 3.308e-8, 7.061e-2, 1.072e-3, 7.081e-3, 2.321e-1, 1.317e-1, 2.477e-2, 6.834e-1]
