from pathlib import Path

from coltrane import initialize

wsgi = initialize(BASE_DIR=Path(__file__).resolve().parent)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line()
