from pathlib import Path
from unittest.mock import ANY, patch

from coltrane import initialize


# from django.conf import settings


DEFAULT_SETTINGS = {
    "BASE_DIR": Path("."),
    "ROOT_URLCONF": "coltrane",
    "DEBUG": True,
    "SECRET_KEY": None,
    "INSTALLED_APPS": ["coltrane"],
    "CACHES": {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
    "MIDDLWARE": [
        "django.middleware.security.SecurityMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ],
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
        }
    ],
    "COLTRAN": {"VIEW_CACHE_SECONDS": 3600},
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
