from importlib.metadata import version
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from coltrane.console import APP_DIR, cli

FILES_PATH = Path(__file__).parent.parent.parent / "coltrane/default-files"


def test_create(tmp_path):
    runner = CliRunner()

    with patch("coltrane.console.get_random_secret_key") as get_random_secret_key:
        get_random_secret_key.return_value = "this-is-a-test"

        with runner.isolated_filesystem(temp_dir=tmp_path) as temp_dir:
            result = runner.invoke(cli, ["create"])
            assert result.exit_code == 0

            path_temp_dir = Path(temp_dir) / APP_DIR

            app_file = path_temp_dir / "app.py"
            assert app_file.exists()

            expected_app_py = (FILES_PATH / "app.py").read_text().replace("__coltrane_version__", version("coltrane"))
            assert app_file.read_text() == expected_app_py

            env_file = path_temp_dir / ".env"
            assert env_file.exists()
            assert env_file.read_text() == (FILES_PATH / "env").read_text() + "SECRET_KEY=this-is-a-test"

            content_dir = path_temp_dir / "content"
            assert content_dir.exists()

            assert (content_dir / "index.md").exists()
            assert (content_dir / "index.md").read_text() == "# index.md"

            data_dir = path_temp_dir / "data"
            assert data_dir.exists()

            assert (
                result.stdout
                == """Start creating files...

- Create .gitignore
- Create Dockerfile
- Create pyproject.toml
- Create README.md
- Create site/.env
- Create site/.watchmanconfig
- Create site/app.py
- Set site/app.py as executable
- Create site/gunicorn.conf.py
- Create site/content directory
- Create site/data directory
- Create site/static directory
- Create site/templates directory

For local development: coltrane play
Build static HTML: coltrane record
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

For local development: coltrane play
Build static HTML: coltrane record
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
