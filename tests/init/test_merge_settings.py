from copy import deepcopy
from pathlib import Path
from unittest.mock import ANY, patch

from coltrane import _merge_settings
from tests.init.test_initialize import (  # type: ignore
    DEFAULT_SETTINGS,
    _get_settings,
)


@patch("coltrane.is_whitenoise_installed", return_value=False)
@patch("coltrane.is_django_compressor_installed", return_value=False)
@patch("coltrane.is_django_unicorn_installed", return_value=False)
@patch("coltrane.is_unicorn_module_available", return_value=False)
def test_merge_settings_no_extras_with_args(*args):
    expected = deepcopy(DEFAULT_SETTINGS)
    expected["INSTALLED_APPS"].append("django_browser_reload")
    expected["MIDDLEWARE"].append("django_browser_reload.middleware.BrowserReloadMiddleware")

    actual = _merge_settings(Path("."), {})

    assert actual == expected


@patch("coltrane.is_whitenoise_installed", return_value=True)
@patch("coltrane.is_django_compressor_installed", return_value=False)
@patch("coltrane.is_django_unicorn_installed", return_value=False)
@patch("coltrane.is_unicorn_module_available", return_value=False)
def test_merge_settings_with_whitenoise(*args):
    expected = _get_settings()
    del expected["ENV"]

    expected.update(
        {
            "WHITENOISE_MANIFEST_STRICT": False,
            "STATICFILES_STORAGE": ANY,
        }
    )

    expected["INSTALLED_APPS"].insert(0, "whitenoise.runserver_nostatic")
    expected["MIDDLEWARE"].insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    actual = _merge_settings(Path("."), {})

    assert actual == expected


@patch("coltrane.is_whitenoise_installed", return_value=False)
@patch("coltrane.is_django_compressor_installed", return_value=False)
@patch("coltrane.is_django_unicorn_installed", return_value=True)
@patch("coltrane.is_unicorn_module_available", return_value=False)
def test_merge_settings_with_django_unicorn(*args):
    actual = _merge_settings(Path("."), {})
    installed_apps = actual["INSTALLED_APPS"]

    assert "django_unicorn" in installed_apps
    assert "unicorn" not in installed_apps


@patch("coltrane.is_whitenoise_installed", return_value=False)
@patch("coltrane.is_django_compressor_installed", return_value=False)
@patch("coltrane.is_django_unicorn_installed", return_value=True)
@patch("coltrane.is_unicorn_module_available", return_value=True)
def test_merge_settings_with_django_unicorn_and_unicorn(*args):
    actual = _merge_settings(Path("."), {})
    installed_apps = actual["INSTALLED_APPS"]

    assert "django_unicorn" in installed_apps
    assert "unicorn" in installed_apps


@patch("coltrane.is_whitenoise_installed", return_value=False)
@patch("coltrane.is_django_compressor_installed", return_value=False)
@patch("coltrane.is_django_unicorn_installed", return_value=False)
@patch("coltrane.is_unicorn_module_available", return_value=False)
def test_merge_settings_no_django_unicorn(*args):
    actual = _merge_settings(Path("."), {})
    installed_apps = actual["INSTALLED_APPS"]

    assert "django_unicorn" not in installed_apps
    assert "unicorn" not in installed_apps
