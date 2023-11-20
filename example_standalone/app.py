#!/usr/bin/env python

from pathlib import Path

from django.core.management import execute_from_command_line

from coltrane import initialize

# Pass in this file's parent as the BASE_DIR because app.py lives in a sub-folder
wsgi = initialize(BASE_DIR=Path(__file__).resolve().parent)

if __name__ == "__main__":
    execute_from_command_line()
