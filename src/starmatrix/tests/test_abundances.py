import pytest
import numpy as np
import starmatrix.settings as settings
from starmatrix.abundances import Abundances, select_abundances
from starmatrix.abundances import AndersGrevesse1989, GrevesseSauval1998, Asplund2005, Asplund2009, Heger2010, Lodders2019


@pytest.fixture
def available_abundances():
    """
    Fixture returning all the valid values for the solar abundance setting
    """
    return settings.valid_values["sol_ab"]


def test_select_abundances():
    strings = ["ag89", "gs98", "as05", "as09", "he10", "lo19"]
    classes = [AndersGrevesse1989, GrevesseSauval1998, Asplund2005, Asplund2009, Heger2010, Lodders2019]

    for i in range(len(strings)):
        abundance_instance = select_abundances(strings[i], 0.033)
        assert type(abundance_instance) == classes[i]
        assert abundance_instance.z == 0.033


def test_abundances_classes_presence(available_abundances):
    for abundance in available_abundances:
        assert select_abundances(abundance, 0.02) is not None


def test_description_presence(available_abundances):
    for abundance in available_abundances:
        assert select_abundances(abundance, 0.02).description() != Abundances(0.02).description()


def test_feh_with_z_zero():
    assert Abundances(0).feh() == -20


def test_feh_with_z_non_zero(available_abundances):
    for abundance in available_abundances:
        assert select_abundances(abundance, 0.025).feh() > 0.0


def test_h_he4_values(available_abundances):
    for abundance in available_abundances:
        assert select_abundances(abundance, 0.025).h() > 0.0
        assert select_abundances(abundance, 0.025).he4() > 0.0


def test_elements_value_presence(available_abundances):
    for abundance in available_abundances:
        elements = np.array(list(select_abundances(abundance, 0.025).elements().values()))
        assert np.all(elements > 0.0)
        assert np.all(elements < 1.0)


def test_abundance_values_presence(available_abundances):
    for abundance in available_abundances:
        abundance_values = np.array(list(select_abundances(abundance, 0.025).abundance().values()))
        assert np.all(abundance_values > 0.0)


def test_cri_lim_exception(available_abundances):
    for abundance in available_abundances:
        normal = select_abundances(abundance, 0.02).abundance()
        cri_lim_corrected = select_abundances(abundance, 0.02).corrected_abundance_CRI_LIM()
        assert normal == cri_lim_corrected

        normal = select_abundances(abundance, 0.013).abundance()
        cri_lim_corrected = select_abundances(abundance, 0.013).corrected_abundance_CRI_LIM()
        assert normal != cri_lim_corrected
