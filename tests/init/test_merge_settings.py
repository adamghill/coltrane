from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from coltrane import _merge_settings
from tests.init.test_initialize import DEFAULT_SETTINGS, _get_settings_with_whitenoise


@patch("coltrane._is_whitenoise_installed", return_value=True)
def test_merge_settings_with_whitenoise(_is_whitenoise_installed):
    expected = deepcopy(_get_settings_with_whitenoise())
    actual = _merge_settings(Path("."), {})

    assert actual == expected


@patch("coltrane._is_whitenoise_installed", return_value=False)
def test_merge_settings_no_whitenoise(_is_whitenoise_installed):
    expected = deepcopy(DEFAULT_SETTINGS)
    expected["INSTALLED_APPS"].append("django_browser_reload")
    expected["MIDDLEWARE"].append(
        "django_browser_reload.middleware.BrowserReloadMiddleware"
    )

    actual = _merge_settings(Path("."), {})

    assert actual == expected
