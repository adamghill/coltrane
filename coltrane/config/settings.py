from os import getenv
from typing import Any, Dict, List, Optional

from django.conf import settings

# List of all available `Markdown2` extras: https://github.com/trentm/python-markdown2/wiki/Extras
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

# List of available `mistune` plugins: https://mistune.lepture.com/en/latest/plugins.html
DEFAULT_MISTUNE_PLUGINS = [
    "strikethrough",
    "footnotes",
    "table",
    "task_lists",
    "def_list",
    "abbr",
    "mark",
    "insert",
    "superscript",
    "subscript",
]

# Used to look at environment variables to merge into settings
DEFAULT_COLTRANE_SETTINGS = {
    "TITLE": "",
    "DESCRIPTION": "",
    "SITE_URL": "",
    "MARKDOWN_RENDERER": "markdown2",
    "MARKDOWN_EXTRAS": DEFAULT_MARKDOWN_EXTRAS,
    "MISTUNE_PLUGINS": DEFAULT_MISTUNE_PLUGINS,
    "EXTRA_FILE_NAMES": [],
    "CONTENT_DIRECTORY": "content",
    "DATA_DIRECTORY": "data",
}


def get_coltrane_settings() -> Dict:
    """
    Get the `COLTRANE` settings from the settings file.
    """

    if hasattr(settings, "COLTRANE"):
        if not isinstance(settings.COLTRANE, dict):
            raise TypeError("COLTRANE settings should be a dictionary")

        return settings.COLTRANE

    return DEFAULT_COLTRANE_SETTINGS


def get_markdown_renderer() -> str:
    """
    Get the markdown renderer. Either "markdown2" or "mistune".
    """

    markdown_renderer = get_coltrane_settings().get("MARKDOWN_RENDERER", "markdown2")

    if markdown_renderer not in ["markdown2", "mistune"]:
        raise AssertionError("Invalid markdown renderer")

    return markdown_renderer


def get_markdown_extras() -> List[str]:
    """
    Get the `markdown2` extras.
    """

    return get_coltrane_settings().get("MARKDOWN_EXTRAS", DEFAULT_MARKDOWN_EXTRAS)


def get_mistune_plugins() -> List[str]:
    """
    Get the `mistune` plugins.
    """

    return get_coltrane_settings().get("MISTUNE_PLUGINS", DEFAULT_MISTUNE_PLUGINS)


def get_site_url() -> Optional[str]:
    """
    Get the configured site.
    """

    return get_coltrane_settings().get("SITE_URL")


def get_title() -> Optional[str]:
    """
    Get the configured title.
    """

    return get_coltrane_settings().get("TITLE")


def get_description() -> Optional[str]:
    """
    Get the configured description.
    """

    return get_coltrane_settings().get("DESCRIPTION")


def get_data_directory() -> str:
    """
    Get the configured data directory.
    """

    return get_coltrane_settings().get("DATA_DIRECTORY", DEFAULT_COLTRANE_SETTINGS["DATA_DIRECTORY"])


def get_content_directory() -> str:
    """
    Get the configured data directory.
    """

    return get_coltrane_settings().get("CONTENT_DIRECTORY", DEFAULT_COLTRANE_SETTINGS["CONTENT_DIRECTORY"])


def get_extra_file_names() -> List[str]:
    return get_coltrane_settings().get(
        "EXTRA_FILE_NAMES",
        [],
    )
