from pathlib import Path
from unittest.mock import ANY, patch

from coltrane import (
    DEFAULT_CACHES_SETTINGS,
    DEFAULT_COLTRANE_SETTINGS,
    DEFAULT_INSTALLED_APPS,
    DEFAULT_MIDDLEWARE_SETTINGS,
    _get_default_template_settings,
    initialize,
)


base_dir = Path(".")

DEFAULT_SETTINGS = {
    "BASE_DIR": base_dir,
    "ROOT_URLCONF": "coltrane",
    "DEBUG": True,
    "SECRET_KEY": ANY,
    "INSTALLED_APPS": DEFAULT_INSTALLED_APPS,
    "CACHES": DEFAULT_CACHES_SETTINGS,
    "MIDDLWARE": DEFAULT_MIDDLEWARE_SETTINGS,
    "TEMPLATES": _get_default_template_settings(base_dir),
    "INTERNAL_IPS": [],
    "COLTRANE": DEFAULT_COLTRANE_SETTINGS,
}


@patch("coltrane._configure_settings")
def test_initialize_no_base_dir(_configure_settings):
    initialize()

    _configure_settings.assert_called_once_with(DEFAULT_SETTINGS)


@patch("coltrane._configure_settings")
def test_initialize_with_base_dir(_configure_settings):
    initialize(base_dir=Path("test"))

    expected = DEFAULT_SETTINGS.copy()
    expected["BASE_DIR"] = Path("test")
    expected["TEMPLATES"][0]["DIRS"] = [Path("test") / "templates"]

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane._configure_settings")
def test_initialize_with_base_dir_as_string(_configure_settings):
    initialize(base_dir="test")

    expected = DEFAULT_SETTINGS.copy()
    expected["BASE_DIR"] = Path("test")
    expected["TEMPLATES"][0]["DIRS"] = [Path("test") / "templates"]

    _configure_settings.assert_called_once_with(expected)
