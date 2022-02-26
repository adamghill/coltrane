from unittest.mock import patch

from click.testing import CliRunner

from coltrane.console import cli


def test_record():
    runner = CliRunner()

    with patch("coltrane.console._run_management_command") as _run_management_command:
        result = runner.invoke(cli, ["record"])
        assert result.exit_code == 0

        _run_management_command.assert_called_once_with("build")


def test_build_alias():
    runner = CliRunner()

    with patch("coltrane.console._run_management_command") as _run_management_command:
        result = runner.invoke(cli, ["build"])
        assert result.exit_code == 0

        _run_management_command.assert_called_once_with("build")


def test_rec_alias():
    runner = CliRunner()

    with patch("coltrane.console._run_management_command") as _run_management_command:
        result = runner.invoke(cli, ["rec"])
        assert result.exit_code == 0

        _run_management_command.assert_called_once_with("build")


@patch("coltrane.console._run_management_command")
def test_record_force(_run_management_command):
    runner = CliRunner()
    runner.invoke(cli, ["record", "--force"])

    _run_management_command.assert_called_once_with("build", "--force")


@patch("coltrane.console._run_management_command")
def test_record_output(_run_management_command):
    runner = CliRunner()
    runner.invoke(cli, ["record", "--output", "public"])

    _run_management_command.assert_called_once_with("build", "--output", "public")


@patch("coltrane.console._run_management_command")
def test_record_threads(_run_management_command):
    runner = CliRunner()
    runner.invoke(cli, ["record", "--threads", "3"])

    _run_management_command.assert_called_once_with("build", "--threads", "3")


@patch("coltrane.console._run_management_command")
def test_record_ignore(_run_management_command):
    runner = CliRunner()
    runner.invoke(cli, ["record", "--ignore"])

    _run_management_command.assert_called_once_with("build", "--ignore")
