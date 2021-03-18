
"""
Datasets of Supernova ejections for different metallicities

"""

sn_elements_list = ["He4", "C12", "C13", "N14", "O16", "Ne", "Mg", "Si", "S", "Ca", "Fe"]


def empty_yields_set():
    return dict(zip(sn_elements_list, [0.0 for i in range(11)]))


def yields(dataset_key, feh):
    datasets = {
        "iwa1998": yields_from_iwamoto,
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

