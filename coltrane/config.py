from os import getcwd
from pathlib import Path

from django.conf import settings


def get_base_directory() -> Path:
    if hasattr(settings, "BASE_DIR"):
        if isinstance(settings.BASE_DIR, str):
            return Path(settings.BASE_DIR)

        return settings.BASE_DIR

    return Path(getcwd())


def get_data_json() -> Path:
    return get_base_directory() / "data.json"


def get_data_directory() -> Path:
    return get_base_directory() / "data"


def get_content_directory() -> Path:
    return get_base_directory() / "content"


def get_output_directory() -> Path:
    return get_base_directory() / "output"


def get_output_json() -> Path:
    return get_base_directory() / "output.json"
