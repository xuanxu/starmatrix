import pytest
from pytest_mock import mocker
import numpy as np
import starmatrix.constants as constants
import starmatrix.settings as settings
import starmatrix.elements as elements
import starmatrix.abundances as abundances
import starmatrix.matrix as matrix


def test_q_index():
    assert matrix.q_index("H") == 0
    assert matrix.q_index("Fe") == 14


def resize_matrix():
    expected_size = (constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS)
    assert np.zeros((constants.Q_MATRIX_ROWS + 5, constants.Q_MATRIX_COLUMNS + 33)).shape == expected_size


def test_empty_q_matrix():
    empty_matrix = matrix.empty_q_matrix()

    assert empty_matrix.shape == (15, 15)
    assert np.all([i == 0 for i in empty_matrix])


def test_matrices_are_empty_if_not_enough_mass():
    m = constants.M_MIN - 0.001
    test_settings = {
        "z": 0.03,
        "abundances": abundances.select_abundances(np.random.choice(settings.valid_values["sol_ab"]), 0.03),
        "expelled": elements.Expelled(settings.default["expelled_elements_filename"]),
    }

    assert np.all([i == 0 for i in matrix.q(m, test_settings)])
    assert np.all([i == 0 for i in matrix.q_sn(m)])


def test_q_sn_size():
    for m in [0.8, 1, 2, 4, 6, (np.random.rand() * 8), 8, 10, 40, 90]:
        for feh in [-3.3, -1.3, -0.3, 0., 0.17, 0.3, 0.4]:  # test z from 0.00001 to 0.05

            q_supernovae = matrix.q_sn(m, feh=feh)

            assert q_supernovae.shape == (constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS)


def test_q_size():
    for m in [0.8, 1, 2, 4, 6, 8, 10, 40, 90]:
        for z in [0., 0.001, 0.01, 0.02, 0.03, 0.04, 0.05]:
            test_settings = {
                "z": z,
                "abundances": abundances.select_abundances(np.random.choice(settings.valid_values["sol_ab"]), z),
                "expelled": elements.Expelled(settings.default["expelled_elements_filename"]),
            }

            q = matrix.q(m, test_settings)

            assert q.shape == (constants.Q_MATRIX_ROWS, constants.Q_MATRIX_COLUMNS)


def test_q_applies_yield_corrections(mocker):
    m = constants.M_MIN + np.random.rand() * 40
    expelled = elements.Expelled(settings.default["expelled_elements_filename"])
    test_settings = {
                "z": 0.02,
                "abundances": abundances.select_abundances(np.random.choice(settings.valid_values["sol_ab"]), 0.02),
                "expelled": expelled,
                "yield_corrections": {"Mg": 2, "Fe": 3.45}
            }

    mocker.spy(expelled, "for_mass")
    q = matrix.q(m, test_settings)
    expelled.for_mass.assert_called_once_with(m, {"Mg": 2, "Fe": 3.45})


def test_q_with_no_yield_corrections(mocker):
    m = constants.M_MIN + np.random.rand() * 40
    expelled = elements.Expelled(settings.default["expelled_elements_filename"])
    test_settings = {
                "z": 0.02,
                "abundances": abundances.select_abundances(np.random.choice(settings.valid_values["sol_ab"]), 0.02),
                "expelled": expelled,
            }

    mocker.spy(expelled, "for_mass")
    q = matrix.q(m, test_settings)
    expelled.for_mass.assert_called_once_with(m, {})


def test_cri_lim_exception(mocker):
    test_settings = {
        "z": 0.03,
        "abundances": abundances.select_abundances(np.random.choice(settings.valid_values["sol_ab"]), 0.03),
        "expelled": elements.Expelled(settings.default["expelled_elements_filename"]),
    }
    mocker.spy(abundances.Abundances, "abundance")
    mocker.spy(abundances.Abundances, "corrected_abundance_CRI_LIM")

    q = matrix.q(4, test_settings)

    abundances.Abundances.abundance.assert_called_once()
    abundances.Abundances.corrected_abundance_CRI_LIM.assert_not_called()

    test_settings["expelled"].cri_lim_yields = True

    q = matrix.q(4, test_settings)

    abundances.Abundances.corrected_abundance_CRI_LIM.assert_called_once()
