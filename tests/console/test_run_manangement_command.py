from unittest.mock import patch

from coltrane.console import _run_manangement_command


def test_run_manangement_command(tmp_path):
    with patch("coltrane.console.getcwd") as getcwd:
        getcwd.return_value = str(tmp_path)

        with patch("coltrane.console.run_process") as run_process:
            _run_manangement_command("test-command", "arg1")

            run_process.assert_called_once_with(
                [tmp_path / "app.py", "test-command", "arg1"]
            )

        getcwd.assert_called_once()
