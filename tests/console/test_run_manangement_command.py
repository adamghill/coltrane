from pathlib import Path
from unittest.mock import patch

from coltrane.console import APP_DIR, _run_management_command


def test_run_management_command(tmp_path):
    (Path(tmp_path) / APP_DIR).mkdir(exist_ok=True)
    (Path(tmp_path) / APP_DIR / "app.py").touch()

    with patch("coltrane.console.getcwd") as getcwd:
        getcwd.return_value = str(tmp_path)

        with patch("coltrane.console.run_process") as run_process:
            _run_management_command("test-command", "arg1")

            run_process.assert_called_once_with([tmp_path / APP_DIR / "app.py", "test-command", "arg1"])

        getcwd.assert_called_once()
