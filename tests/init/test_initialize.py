from pathlib import Path
from unittest.mock import ANY, patch

from coltrane import (
    DEFAULT_CACHES_SETTINGS,
    DEFAULT_COLTRANE_SETTINGS,
    DEFAULT_MIDDLEWARE_SETTINGS,
    DEFAULT_TEMPLATES_SETTINGS,
    initialize,
)


DEFAULT_SETTINGS = {
    "BASE_DIR": Path("."),
    "ROOT_URLCONF": "coltrane",
    "DEBUG": True,
    "SECRET_KEY": ANY,
    "INSTALLED_APPS": ["coltrane"],
    "CACHES": DEFAULT_CACHES_SETTINGS,
    "MIDDLWARE": DEFAULT_MIDDLEWARE_SETTINGS,
    "TEMPLATES": DEFAULT_TEMPLATES_SETTINGS,
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

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane._configure_settings")
def test_initialize_with_base_dir_as_string(_configure_settings):
    initialize(base_dir="test")

    expected = DEFAULT_SETTINGS.copy()
    expected["BASE_DIR"] = Path("test")

    _configure_settings.assert_called_once_with(expected)
