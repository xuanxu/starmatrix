import pytest
from pytest_mock import mocker
import argparse, os, shutil
import intergalactic.cli as cli
import intergalactic.model as model
import intergalactic.settings as settings

@pytest.fixture
def deactivate_os_actions(mocker):
    """
    Fixture to disable all calls to the operating system (mkdir, rm, copy...)
    """
    mocker.patch.object(model, 'Model')
    mocker.patch.object(model.Model, 'run')
    mocker.patch.object(os, 'makedirs')
    mocker.patch.object(shutil, 'rmtree')
    mocker.patch.object(shutil, 'copy')
    mocker.patch.object(argparse.ArgumentParser, 'parse_args')
    argparse.ArgumentParser.parse_args.return_value = argparse.Namespace(generate_config=False, config=None)
    os.makedirs.return_value = True
    shutil.rmtree.return_value = True

@pytest.fixture
def mock_config_file(mocker):
    """
    Fixture mocking contents of a config file reading
    """
    config_file_content = "m_max: 33.0\ntotal_time_steps: 123"
    mocked_file = mocker.mock_open(read_data=config_file_content)
    mocker.patch.object(cli, 'open', mocked_file)
    mocker.spy(cli, "read_config_file")
    return {'m_max': 33.0, 'total_time_steps': 123}

def test_option_generate_config(mocker, deactivate_os_actions):
    argparse.ArgumentParser.parse_args.return_value = argparse.Namespace(generate_config=True)
    mocker.spy(cli, "create_template_config_file")
    cli.main()
    cli.create_template_config_file.assert_called()

def test_option_config(mocker, deactivate_os_actions, mock_config_file):
    argparse.ArgumentParser.parse_args.return_value = argparse.Namespace(generate_config=False, config='ejectas.dat')
    cli.main()
    cli.read_config_file.assert_called_once_with('ejectas.dat')

def test_model_is_configured_properly(mocker, deactivate_os_actions, mock_config_file):
    argparse.ArgumentParser.parse_args.return_value = argparse.Namespace(generate_config=False, config='ejectas.dat')
    cli.main()
    expected_context = {**settings.default, **mock_config_file}

    model.Model.assert_called_once_with(expected_context)
    model.Model(expected_context).run.assert_called()

def test_model_is_run(mocker, deactivate_os_actions):
    cli.main()
    model.Model.assert_called()
    model.Model(settings.default).run.assert_called()
