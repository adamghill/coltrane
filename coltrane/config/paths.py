from os import getcwd
from pathlib import Path
from typing import Iterable

from django.conf import settings

from coltrane.config.settings import get_content_directory as get_content_directory_setting
from coltrane.config.settings import get_data_directory as get_data_directory_setting
from coltrane.config.settings import get_extra_file_names


def get_base_directory() -> Path:
    """
    Get base directory from settings or return the default of the current directory.
    """

    if hasattr(settings, "BASE_DIR"):
        return Path(settings.BASE_DIR)

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

    return get_base_directory() / get_data_directory_setting()


def get_content_directory() -> Path:
    """
    Get the path of the markdown `content` directory.
    """

    return get_base_directory() / get_content_directory_setting()


def get_templates_directory() -> Path:
    """Get the path of the HTML templates directory."""

    # TODO: Support other directories defined in django.conf.settings.TEMPLATES.DIRS.
    return get_base_directory() / "templates"


def get_extra_file_paths() -> Iterable[Path]:
    for file_name in get_extra_file_names():
        file_path = get_file_path(file_name)

        if file_path.exists():
            yield file_path


def get_file_path(file_name: str) -> Path:
    """
    Get the path of a file in the content directory.
    """

    return get_content_directory() / file_name


def get_output_directory_name() -> str:
    """
    Gets the output directory name from settings if it is set. Defaults to "output".
    """

    output_directory_name = "output"

    try:
        output_directory_name = settings.COLTRANE["OUTPUT"]["PATH"]
    except (AttributeError, KeyError):
        pass

    return output_directory_name


def get_output_directory() -> Path:
    """
    Get the path that HTML files will be output to.
    """

    try:
        return Path(settings.COLTRANE["OUTPUT"]["DIRECTORY"])
    except (AttributeError, KeyError):
        pass

    return get_base_directory() / get_output_directory_name()


def get_output_json() -> Path:
    """
    Get the path of the JSON manifest `output.json` file.
    """

    return get_base_directory() / "output.json"


def get_staticfiles_json() -> Path:
    """
    Get the path of Django's `staticfiles.json` manifest file.
    """

    return Path(settings.STATIC_ROOT) / "staticfiles.json"


def get_output_static_directory() -> Path:
    """
    Get the path of Django's static path.
    """

    return Path(settings.STATIC_ROOT)
