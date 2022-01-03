"""
A little wrapper CLI over a few Django management commands.
"""

from os import getcwd
from pathlib import Path
from stat import S_IEXEC
from subprocess import run as run_process

import click


DEFAULT_APP = """#!/usr/bin/env python

from django.core.management import execute_from_command_line

from coltrane import initialize


wsgi = initialize()

if __name__ == "__main__":
    execute_from_command_line()
"""

DEFAULT_ENV = """DEBUG=True
SECRET_KEY=this-is-a-secret
"""


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


@click.command(help="Create a coltrane site.")
def init():
    app_file = Path("app.py")

    if not app_file.exists():
        print("Creating app.py...")
        app_file.write_text(DEFAULT_APP)
        print("Set app.py as executable...")
        app_file.chmod(app_file.stat().st_mode | S_IEXEC)

        print("Creating .env...")
        Path(".env").write_text(DEFAULT_ENV)

        print("Creating content directory...")
        Path("content").mkdir()
        (Path("content") / "index.md").write_text("# index.md")

        print("Creating data directory...")
        Path("data").mkdir()

        print("Finished!")
        print()
        print(
            "Run `coltrane serve` for local development or `coltrane build` to generate HTML output."
        )


def _get_manage_file_path(manage: str) -> Path:
    current_directory = getcwd()
    file_path = Path(current_directory) / manage

    if not file_path.exists():
        # Try the default manage.py
        file_path = Path(current_directory) / "manage.py"

    return file_path


@click.command(help="Start a local development server; alias: serve.")
@click.option("--port", default=8000, help="Port to serve from")
@click.option("--manage", default="app.py", help="File name for Django's manage.py")
def play(port, manage):
    file_path = _get_manage_file_path(manage)

    run_process(
        [
            file_path,
            "runserver",
            f"0:{port}",
        ]
    )


@click.command(help="Generates HTML output; alias: build.")
@click.option("--output", default="output", help="Output directory")
@click.option("--manage", default="app.py", help="File name for Django's manage.py")
def record(output, manage):
    file_path = _get_manage_file_path(manage)

    run_process(
        [
            file_path,
            "build",
            output,
        ]
    )


cli.add_command(init)
cli.add_command(play)
cli.add_command(record)


ALIASES = {
    "serve": play,
    "pl": play,
    "build": record,
    "rec": record,
}
