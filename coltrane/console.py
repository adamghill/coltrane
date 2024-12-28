"""
A little wrapper CLI over a few Django management commands.
"""

from importlib.metadata import version
from os import environ, getcwd
from pathlib import Path
from stat import S_IEXEC
from subprocess import run as run_process

import rich_click as click
from click_aliases import ClickAliasedGroup
from django.core.management.utils import get_random_secret_key
from rich_click.rich_command import RichCommand

FILES_PATH = Path(__file__).parent / "default-files"
APP_DIR = "site"


def _run_management_command(command_name, *args):
    current_directory = getcwd()
    file_path = Path(current_directory) / "app.py"

    if not file_path.exists():
        file_path = Path(current_directory) / APP_DIR / "app.py"

    if not file_path.exists():
        file_path = Path(current_directory) / "sites" / "app.py"

    if not file_path.exists():
        raise Exception("app.py could not be found.")

    run_process([file_path, command_name, *list(args)])  # noqa: S603, PLW1510


def _copy_file(file_name, in_app_dir=False) -> Path:
    default_file_name = file_name

    if file_name.startswith("."):
        default_file_name = file_name[1:]

    with (FILES_PATH / default_file_name).open() as f:
        file_text = f.read()

        if "__coltrane_version__" in file_text:
            coltrane_version = version("coltrane")
            file_text = file_text.replace("__coltrane_version__", coltrane_version)

        if "__app_name__" in file_text:
            current_directory = getcwd().split("/")
            app_name = current_directory[len(current_directory) - 1 :][0]

            file_text = file_text.replace("__app_name__", app_name)

        path = Path(file_name)

        if in_app_dir:
            path = APP_DIR / path

        path.write_text(file_text)

        return path


class AliasedCommands(ClickAliasedGroup, RichCommand):
    pass


@click.group(cls=AliasedCommands, help="Runs commands for coltrane.")
@click.version_option()
def cli():
    pass


@cli.command(help="Create a new coltrane site. Alias: init.", aliases=["init"])
@click.option("--force/--no-force", default=False, help="Force creating a new site")
def create(force):
    app_file = Path("app.py")

    if not app_file.exists():
        app_file = APP_DIR / Path("app.py")

    if app_file.exists() and not force:
        click.secho("Skip project creation because app.py already exists.", fg="red")
    else:
        click.secho("Start creating files...\n", fg="yellow")
        Path(APP_DIR).mkdir(exist_ok=True)
        (APP_DIR / Path("__init__.py")).touch()

        click.secho("- Create .gitignore")
        _copy_file(".gitignore")

        click.secho("- Create Dockerfile")
        _copy_file("Dockerfile")

        click.secho("- Create pyproject.toml")
        _copy_file("pyproject.toml")

        click.secho("- Create README.md")
        _copy_file("README.md")

        click.secho(f"- Create {APP_DIR}/.env")
        env_file = _copy_file(".env", in_app_dir=True)

        # Add randomly generated secret key
        with env_file.open("a") as f:
            f.write(f"SECRET_KEY={get_random_secret_key()}")

        click.secho(f"- Create {APP_DIR}/.watchmanconfig")
        _copy_file(".watchmanconfig", in_app_dir=True)

        click.secho(f"- Create {APP_DIR}/app.py")
        app_file = _copy_file("app.py", in_app_dir=True)

        click.secho(f"- Set {APP_DIR}/app.py as executable")
        app_file.chmod(app_file.stat().st_mode | S_IEXEC)

        click.secho(f"- Create {APP_DIR}/gunicorn.conf.py")
        _copy_file("gunicorn.conf.py", in_app_dir=True)

        click.secho("- Create site/content directory")
        (APP_DIR / Path("content")).mkdir(exist_ok=True)
        (APP_DIR / Path("content") / "index.md").write_text("# index.md")

        click.secho("- Create site/data directory")
        (APP_DIR / Path("data")).mkdir(exist_ok=True)

        click.secho("- Create site/static directory")
        (APP_DIR / Path("static")).mkdir(exist_ok=True)

        click.secho("- Create site/templates directory")
        (APP_DIR / Path("templates")).mkdir(exist_ok=True)

    click.secho()
    click.secho("For local development: ", nl=False, fg="green")
    click.secho("coltrane play")
    click.secho("Build static HTML: ", nl=False, fg="green")
    click.secho("coltrane record")


@cli.command(help="Start a local development server. Alias: serve.", aliases=["serve"])
@click.option("--config", default="coltrane.toml", help="Config file name")
@click.option("--port", default=8000, help="Port to serve localhost from")
def play(config, port):
    environ.setdefault("COLTRANE_CONFIG_FILE", config)
    _run_management_command("runserver", f"0:{port}")


@cli.command(help="Generates HTML output. Aliases: rec, build.", aliases=["rec", "build"])
@click.option("--force/--no-force", default=False, help="Force HTML generation")
@click.option("--threads", type=int, help="Number of threads to use when generating static files")
@click.option("--output", help="Output directory")
@click.option("--ignore/--no-ignore", default=False, help="Ignore errors")
def record(force, threads, output, ignore):
    args = []

    if force:
        args.append("--force")

    if output:
        args.append("--output")
        args.append(output)

    if threads:
        args.append("--threads")
        args.append(str(threads))

    if ignore:
        args.append("--ignore")

    _run_management_command("build", *args)
