from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from coltrane.console import DEFAULT_APP, DEFAULT_ENV, cli


def test_create(tmp_path):
    runner = CliRunner()

    with patch("coltrane.console.get_random_secret_key") as get_random_secret_key:
        get_random_secret_key.return_value = "this-is-a-test"

        with runner.isolated_filesystem(temp_dir=tmp_path) as temp_dir:
            result = runner.invoke(cli, ["create"])
            assert result.exit_code == 0

            temp_dir = Path(temp_dir)

            app_file = temp_dir / "app.py"
            assert app_file.exists()
            assert app_file.read_text() == DEFAULT_APP

            env_file = temp_dir / ".env"
            assert env_file.exists()
            assert env_file.read_text() == DEFAULT_ENV + "this-is-a-test"

            content_dir = temp_dir / "content"
            assert content_dir.exists()

            assert (content_dir / "index.md").exists()
            assert (content_dir / "index.md").read_text() == "# index.md"

            data_dir = temp_dir / "data"
            assert data_dir.exists()

            assert (
                result.stdout
                == """Start creating files...

- Create app.py
- Set app.py as executable
- Create .env
- Create .watchmanconfig
- Create content directory
- Create data directory

For local development: poetry run coltrane play
Build static HTML: poetry run coltrane record
"""
            )


def test_create_existing_project(tmp_path):
    runner = CliRunner()

    with patch("coltrane.console.get_random_secret_key") as get_random_secret_key:
        get_random_secret_key.return_value = "this-is-a-test"

        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["create"])
            assert result.exit_code == 0

            # Re-run create and make sure app.py check works
            result = runner.invoke(cli, ["create"])
            assert result.exit_code == 0

            assert (
                result.stdout
                == """Skip project creation because app.py already exists.

For local development: poetry run coltrane play
Build static HTML: poetry run coltrane record
"""
            )


def test_init_alias(tmp_path):
    runner = CliRunner()

    with patch("coltrane.console.get_random_secret_key") as get_random_secret_key:
        get_random_secret_key.return_value = "this-is-a-test"

        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(cli, ["init"])
            assert result.exit_code == 0

            assert "Start creating files..." in result.stdout
