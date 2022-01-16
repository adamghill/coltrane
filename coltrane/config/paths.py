from os import getcwd
from pathlib import Path

from django.conf import settings


def get_base_directory() -> Path:
    """
    Get base directory from settings or return the default of the current directory.
    """

    if hasattr(settings, "BASE_DIR"):
        if isinstance(settings.BASE_DIR, str):
            return Path(settings.BASE_DIR)

        return settings.BASE_DIR

    return Path(getcwd())


def get_data_json() -> Path:
    """
    Get the path of the `data.json` file.
    """

    return get_base_directory() / "data.json"


def get_data_directory() -> Path:
    """
    Get the path of the JSON `data` directory.
    """

    return get_base_directory() / "data"


def get_content_directory() -> Path:
    """
    Get the path of the markdown `content` directory.
    """

    return get_base_directory() / "content"


def get_output_directory() -> Path:
    """
    Get the path that HTML files will be output to.
    """

    return get_base_directory() / "output"


def get_output_json() -> Path:
    """
    Get the path of the JSON manifest `output.json` file.
    """

    return get_base_directory() / "output.json"


def get_staticfiles_json() -> Path:
    """
    Get the path of Django's `staticfiles.json` manifest file.
    """

    return settings.STATIC_ROOT / "staticfiles.json"


def get_output_static_directory() -> Path:
    """
    Get the path of Django's static path.
    """

    return settings.STATIC_ROOT
