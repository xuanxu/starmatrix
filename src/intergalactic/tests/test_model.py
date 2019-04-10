import pytest
from pytest_mock import mocker

import numpy
import intergalactic.model
from intergalactic.model import Model
import intergalactic.settings as settings
import intergalactic.imfs as imfs
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
    assert model.sn_rates == []
    assert model.z == params["z"]
    assert model.dtd == dtds.dtd_mannucci_della_valle_panagia
    assert model.m_min == params["m_min"]
    assert model.m_max == params["m_max"]
    assert model.total_time_steps == params["total_time_steps"]

@pytest.fixture
def deactivate_open_files(mocker):
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
    assert len(model.sn_rates) == settings.default["total_time_steps"]
    mocked_file.assert_called_once_with(f"{settings.default['output_dir']}/mass_intervals", "w+")

def test_create_q_matrices(mocker, deactivate_open_files):
    mocked_file = deactivate_open_files
    mocker.spy(numpy, "savetxt")
    model = Model(settings.default)
    model.total_time_steps = 2
    model.mass_intervals = [[1., 8.], [8., 33.]]
    model.sn_rates = [2e-4, 1e-4]
    model.energies = [3e-4, 1.2e-4]

    model.create_q_matrices()

    calls = [mocker.call(f"{settings.default['output_dir']}/imf_supernova_rates", "w+"),
             mocker.call(f"{settings.default['output_dir']}/qm-matrices", "w+")]
    mocked_file.assert_has_calls(calls)
    assert numpy.savetxt.call_count == model.total_time_steps
