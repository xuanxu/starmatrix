import pytest
from pytest_mock import mocker

import numpy
import intergalactic.model
from intergalactic.model import Model
import intergalactic.settings as settings
import intergalactic.imfs as imfs
import intergalactic.functions as functions
import intergalactic.abundances as abundances
import intergalactic.dtds as dtds


def test_model_initialization():
    params = {
        "z": 0.033,
        "sol_ab": "ag89",
        "imf": "chabrier",
        "m_min": 1.1,
        "m_max": 42.0,
        "total_time_steps": 250,
        "dtd_sn": "mdvp"
    }
    validated_params = settings.validate(params)
    model = Model(validated_params)

    assert isinstance(model.initial_mass_function, imfs.Chabrier)
    assert isinstance(model.context["abundances"], abundances.AndersGrevesse1989)
    assert model.context["abundances"].z == params["z"]
    assert model.mass_intervals == []
    assert model.energies == []
    assert model.sn_Ia_rates == []
    assert model.z == params["z"]
    assert model.dtd == dtds.dtd_mannucci_della_valle_panagia
    assert model.m_min == params["m_min"]
    assert model.m_max == params["m_max"]
    assert model.total_time_steps == params["total_time_steps"]


@pytest.fixture
def deactivate_open_files(mocker):
    """
    Fixture to disable opening of files from model
    """
    mocked_file = mocker.mock_open()
    mocker.patch.object(intergalactic.model, 'open', mocked_file)
    return mocked_file


def test_model_run(mocker):
    mocker.patch.object(Model, "explosive_nucleosynthesis")
    mocker.patch.object(Model, "create_q_matrices")
    Model(settings.default).run()

    Model.explosive_nucleosynthesis.assert_called()
    Model.create_q_matrices.assert_called()


def test_explosive_nucleosynthesis(mocker, deactivate_open_files):
    mocked_file = deactivate_open_files
    model = Model(settings.default)
    model.explosive_nucleosynthesis()

    assert len(model.mass_intervals) == settings.default["total_time_steps"]
    assert len(model.energies) == settings.default["total_time_steps"]
    assert len(model.sn_Ia_rates) == settings.default["total_time_steps"]
    mocked_file.assert_called_once_with(f"{settings.default['output_dir']}/mass_intervals", "w+")


def test_create_q_matrices(mocker, deactivate_open_files):
    mocker.spy(functions, "newton_cotes")
    mocked_file = deactivate_open_files
    mocker.spy(numpy, "savetxt")
    model = Model(settings.default)
    model.total_time_steps = 2
    model.mass_intervals = [[1., 8.], [8., 33.]]
    model.sn_Ia_rates = [2e-4, 1e-4]
    model.energies = [3e-4, 1.2e-4]

    model.create_q_matrices()

    calls = [mocker.call(f"{settings.default['output_dir']}/imf_supernova_rates", "w+"),
             mocker.call(f"{settings.default['output_dir']}/qm-matrices", "w+")]
    mocked_file.assert_has_calls(calls)
    functions.newton_cotes.assert_has_calls
    assert numpy.savetxt.call_count == model.total_time_steps


def test_create_q_matrices_all_zeros_files_if_wrong_data(mocker, deactivate_open_files):
    mocker.spy(functions, "newton_cotes")
    mocked_file = deactivate_open_files
    mocker.spy(numpy, "savetxt")
    model = Model(settings.default)
    model.total_time_steps = 2
    model.mass_intervals = [[0., 0.1], [8., 2.]]
    model.energies = [1e-8, -1e-4]

    model.create_q_matrices()

    calls = [mocker.call(f"{settings.default['output_dir']}/imf_supernova_rates", "w+"),
             mocker.call(f"{settings.default['output_dir']}/qm-matrices", "w+")]
    mocked_file.assert_has_calls(calls)
    assert functions.newton_cotes.call_count == 0
    assert numpy.savetxt.call_count == model.total_time_steps


def test_matrix_header():
    model = Model(settings.default)
    assert model.context["matrix_headers"] is True
    assert model._matrix_header(100, 1) == "Q matrix for mass interval: [100, 1]"

    model.context["matrix_headers"] = False
    assert model._matrix_header(100, 1) == ""
