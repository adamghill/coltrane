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
