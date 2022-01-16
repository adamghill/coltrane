"""
A little wrapper CLI over a few Django management commands.
"""

from os import getcwd
from pathlib import Path
from stat import S_IEXEC
from subprocess import run as run_process

from django.core.management.utils import get_random_secret_key

import click


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
SECRET_KEY="""

DEFAULT_WATCHMAN_CONFIG = """{
  "ignore_dirs": ["node_modules"]
}"""


def _run_manangement_command(command_name, *args):
    current_directory = getcwd()
    file_path = Path(current_directory) / "app.py"

    run_process(
        [
            file_path,
            command_name,
        ]
        + list(args)
    )


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


@click.command(help="Create a new coltrane site (create | init).")
def create():
    app_file = Path("app.py")

    if app_file.exists():
        click.secho(
            "Skipping project creation becase the app.py file alrady exists.", fg="red"
        )
    else:
        click.secho("Creating files...", fg="green")
        Path("__init__.py").touch()

        click.secho("Creating app.py...", fg="yellow")
        app_file.write_text(DEFAULT_APP)

        click.secho("Set app.py as executable...", fg="yellow")
        app_file.chmod(app_file.stat().st_mode | S_IEXEC)

        click.secho("Creating .env...", fg="yellow")
        Path(".env").write_text(DEFAULT_ENV + get_random_secret_key())

        click.secho("Creating .watchmanconfig...", fg="yellow")
        Path(".watchmanconfig").write_text(DEFAULT_WATCHMAN_CONFIG)

        click.secho("Creating content directory...", fg="yellow")
        Path("content").mkdir(exist_ok=True)
        (Path("content") / "index.md").write_text("# index.md")

        click.secho("Creating data directory...", fg="yellow")
        Path("data").mkdir(exist_ok=True)

        click.secho("Finished!", fg="green")

    click.secho()

    click.secho("For local development: ", nl=False, fg="green")
    click.secho("poetry run coltrane play")
    click.secho("Generate HTML output: ", nl=False, fg="green")
    click.secho("poetry run coltrane record")


@click.command(help="Start a local development server (play | serve).")
@click.option("--port", default=8000, help="Port to serve localhost from")
def play(port):
    _run_manangement_command("runserver", f"0:{port}")


@click.command(help="Generates HTML output (record | rec | build).")
@click.option("--force/--no-force", default=False, help="Force HTML generation")
def record(force):
    args = []

    if force:
        args = ["--force"]

    _run_manangement_command("build", *args)


cli.add_command(create)
cli.add_command(play)
cli.add_command(record)


ALIASES = {
    "init": create,
    "serve": play,
    "build": record,
    "rec": record,
}
