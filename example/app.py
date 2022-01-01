#!/usr/bin/env python

from pathlib import Path

from django.core.handlers.wsgi import WSGIHandler
from django.core.management import execute_from_command_line

from static_site import initialize

# Pass in this file's parent as the BASE_DIR
initialize(base_dir=Path(__file__).resolve().parent)

application = WSGIHandler()

if __name__ == "__main__":
    execute_from_command_line()
