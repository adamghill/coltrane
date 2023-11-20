"""
A little wrapper CLI over a few Django management commands.
"""

from os import getcwd
from pathlib import Path
from stat import S_IEXEC
from subprocess import run as run_process

import click
import rich_click  # type: ignore
from django.core.management.utils import get_random_secret_key

click.Command.format_help = rich_click.rich_format_help  # type: ignore
click.Group.format_help = rich_click.rich_format_help  # type: ignore


DEFAULT_APP = """#!/usr/bin/env python

from django.core.management import execute_from_command_line

from coltrane import initialize


wsgi = initialize()

if __name__ == "__main__":
    execute_from_command_line()
"""

DEFAULT_ENV = """DEBUG=True
INTERNAL_IPS=127.0.0.1
ALLOWED_HOSTS=
COLTRANE_SITE_URL=
SECRET_KEY="""

DEFAULT_WATCHMAN_CONFIG = """{
  "ignore_dirs": ["node_modules"]
}"""


def _run_management_command(command_name, *args):
    current_directory = getcwd()
    file_path = Path(current_directory) / "app.py"

    run_process([file_path, command_name, *list(args)])  # noqa: S603, PLW1510


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)


@click.group(cls=AliasedGroup, help="Runs commands for coltrane.")
def cli():
    pass


@click.command(help="Create a new coltrane site.")
@click.option("--force/--no-force", default=False, help="Force creating a new site")
def create(force):
    app_file = Path("app.py")

    if app_file.exists() and not force:
        click.secho("Skip project creation because app.py already exists.", fg="red")
    else:
        click.secho("Start creating files...\n", fg="yellow")
        Path("__init__.py").touch()

        click.secho("- Create app.py")
        app_file.write_text(DEFAULT_APP)

        click.secho("- Set app.py as executable")
        app_file.chmod(app_file.stat().st_mode | S_IEXEC)

        click.secho("- Create .env")
        Path(".env").write_text(DEFAULT_ENV + get_random_secret_key())

        click.secho("- Create .watchmanconfig")
        Path(".watchmanconfig").write_text(DEFAULT_WATCHMAN_CONFIG)

        click.secho("- Create content directory")
        Path("content").mkdir(exist_ok=True)
        (Path("content") / "index.md").write_text("# index.md")

        click.secho("- Create data directory")
        Path("data").mkdir(exist_ok=True)

    click.secho()
    click.secho("For local development: ", nl=False, fg="green")
    click.secho("poetry run coltrane play")
    click.secho("Build static HTML: ", nl=False, fg="green")
    click.secho("poetry run coltrane record")


@click.command(help="Start a local development server.")
@click.option("--port", default=8000, help="Port to serve localhost from")
def play(port):
    _run_management_command("runserver", f"0:{port}")


@click.command(help="Generates HTML output.")
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


cli.add_command(create)
cli.add_command(play)
cli.add_command(record)


ALIASES = {
    "init": create,
    "serve": play,
    "build": record,
    "rec": record,
}
