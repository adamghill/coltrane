from os import getenv
from pathlib import Path
from typing import Dict, List, Optional

import msgspec
from django.conf import settings

from coltrane.config.coltrane import Config
from coltrane.exceptions import ColtraneConfigParseError

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
    "MARKDOWN_RENDERER": "mistune",
    "MISTUNE_PLUGINS": DEFAULT_MISTUNE_PLUGINS,
    "EXTRA_FILE_NAMES": [],
    "CONTENT_DIRECTORY": "content",
    "DATA_DIRECTORY": "data",
    "DISABLE_WILDCARD_TEMPLATES": False,
    "IS_SECURE": False,
    "DATA_JSON5": False,
    "SITES": {},
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
    Get the markdown renderer. Defaults to "mistune".
    """

    markdown_renderer = get_coltrane_settings().get("MARKDOWN_RENDERER", "mistune")

    if markdown_renderer not in [
        "mistune",
    ]:
        raise AssertionError("Invalid markdown renderer")

    return markdown_renderer


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
    return get_coltrane_settings().get("EXTRA_FILE_NAMES", [])


def get_disable_wildcard_templates() -> bool:
    return get_coltrane_settings().get("DISABLE_WILDCARD_TEMPLATES", False)


def get_is_secure() -> bool:
    return get_coltrane_settings().get("IS_SECURE", False)


def get_data_json_5() -> bool:
    return get_coltrane_settings().get("DATA_JSON5", False)


# Global config object that is cached in the module
config: Optional[Config] = None


def reset_config_cache():
    global config

    config = None


def get_config(base_dir: Optional[Path] = None) -> Config:
    global config

    if config is not None:
        return config

    if base_dir is None:
        from django.conf import settings

        base_dir = settings.BASE_DIR

    if base_dir is None:
        raise AssertionError(f"Invalid base directory: {base_dir}")

    if isinstance(base_dir, str):
        base_dir = Path(base_dir)

    config_file_name = getenv("COLTRANE_CONFIG_FILE", "coltrane.toml")
    config_file_path = Path(config_file_name)

    potential_config_file_paths = [
        base_dir / "sites" / config_file_path,
        base_dir / "site" / config_file_path,
        base_dir / config_file_path,
    ]

    for path in potential_config_file_paths:
        if path.exists():
            try:
                config = msgspec.toml.decode(path.read_bytes(), type=Config)

                config.base_dir = base_dir
                config.config_file_name = config_file_name
                config.config_file_path = path
                break
            except msgspec.ValidationError as e:
                raise ColtraneConfigParseError(str(e)) from e

    if config is None:
        config = Config(base_dir=base_dir)

    return config
