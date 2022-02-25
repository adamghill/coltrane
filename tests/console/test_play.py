from unittest.mock import patch

from click.testing import CliRunner

from coltrane.console import cli


def test_play():
    runner = CliRunner()

    with patch("coltrane.console._run_management_command") as _run_management_command:
        result = runner.invoke(cli, ["play"])
        assert result.exit_code == 0

        _run_management_command.assert_called_once_with("runserver", "0:8000")


def test_play_with_port():
    runner = CliRunner()

    with patch("coltrane.console._run_management_command") as _run_management_command:
        result = runner.invoke(cli, ["play", "--port=8001"])
        assert result.exit_code == 0

        _run_management_command.assert_called_once_with("runserver", "0:8001")


def test_serve_alias():
    runner = CliRunner()

    with patch("coltrane.console._run_management_command") as _run_management_command:
        result = runner.invoke(cli, ["serve"])
        assert result.exit_code == 0

        _run_management_command.assert_called_once_with("runserver", "0:8000")
