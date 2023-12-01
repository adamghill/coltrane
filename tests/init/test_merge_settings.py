from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from coltrane import _merge_settings
from tests.init.test_initialize import (  # type: ignore
    DEFAULT_SETTINGS,
    _get_settings_with_whitenoise,
)


@patch("coltrane._is_whitenoise_installed", return_value=True)
def test_merge_settings_with_whitenoise(_is_whitenoise_installed):
    expected = deepcopy(_get_settings_with_whitenoise())
    actual = _merge_settings(Path("."), {})

    assert actual == expected


@patch("coltrane._is_whitenoise_installed", return_value=False)
def test_merge_settings_no_whitenoise(_is_whitenoise_installed):
    expected = deepcopy(DEFAULT_SETTINGS)
    expected["INSTALLED_APPS"].append("django_browser_reload")
    expected["MIDDLEWARE"].append("django_browser_reload.middleware.BrowserReloadMiddleware")

    actual = _merge_settings(Path("."), {})

    assert actual == expected


@patch("coltrane._is_django_unicorn_installed", return_value=True)
def test_merge_settings_with_django_unicorn(_is_django_unicorn_installed):
    actual = _merge_settings(Path("."), {})
    installed_apps = actual["INSTALLED_APPS"]

    assert "django_unicorn" in installed_apps
    assert "unicorn" not in installed_apps


def _is_unicorn_module_available(value):
    if value == "unicorn":
        return True

    return False


@patch("coltrane._is_django_unicorn_installed", return_value=True)
@patch("coltrane._is_module_available", side_effect=_is_unicorn_module_available)
def test_merge_settings_with_django_unicorn_and_unicorn(_is_django_unicorn_installed, _is_module_available):
    actual = _merge_settings(Path("."), {})
    installed_apps = actual["INSTALLED_APPS"]

    assert "django_unicorn" in installed_apps
    assert "unicorn" in installed_apps


@patch("coltrane._is_django_unicorn_installed", return_value=False)
def test_merge_settings_no_django_unicorn(_is_django_unicorn_installed):
    actual = _merge_settings(Path("."), {})
    installed_apps = actual["INSTALLED_APPS"]

    assert "django_unicorn" not in installed_apps
    assert "unicorn" not in installed_apps
