from os import getcwd
from pathlib import Path
from typing import Dict

from django.conf import settings


DEFAULT_VIEW_CACHE_SECONDS = 60 * 60

# List of all available extras: https://github.com/trentm/python-markdown2/wiki/Extras
DEFAULT_MARKDOWN_EXTRAS = [
    "fenced-code-blocks",
    "header-ids",
    "metadata",
    "strike",
    "tables",
    "task_list",
    "nofollow",
    "code-friendly",
    "footnotes",
    "numbering",
    "strike",
    "toc",
]
DEFAULT_COLTRANE_SETTINGS = {
    "VIEW_CACHE_SECONDS": DEFAULT_VIEW_CACHE_SECONDS,
    "MARKDOWN_EXTRAS": DEFAULT_MARKDOWN_EXTRAS,
}


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


def get_coltrane_settings() -> Dict:
    """
    Get the `COLTRANE` settings from the settings file.
    """

    if hasattr(settings, "COLTRANE"):
        assert isinstance(
            settings.COLTRANE, dict
        ), "COLTRANE settings should be a dictionary"

        return settings.COLTRANE

    return DEFAULT_COLTRANE_SETTINGS


def get_view_cache_seconds() -> int:
    """
    Get how long to cache the view from settings or return the default of 1 hour.
    """

    return get_coltrane_settings().get("VIEW_CACHE_SECONDS", DEFAULT_VIEW_CACHE_SECONDS)


def get_markdown_extras() -> int:
    """
    Get the markdown extras.
    """

    return get_coltrane_settings().get("MARKDOWN_EXTRAS", DEFAULT_MARKDOWN_EXTRAS)
