from typing import Dict

from django.conf import settings


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
    "MARKDOWN_EXTRAS": DEFAULT_MARKDOWN_EXTRAS,
}


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


def get_markdown_extras() -> int:
    """
    Get the markdown extras.
    """

    return get_coltrane_settings().get("MARKDOWN_EXTRAS", DEFAULT_MARKDOWN_EXTRAS)
