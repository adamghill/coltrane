from copy import deepcopy
from pathlib import Path

import pytest
from django.conf import settings

from coltrane.config.coltrane import Config
from coltrane.config.settings import DEFAULT_COLTRANE_SETTINGS, reset_config_cache


def get_coltrane_settings():
    coltrane_settings = deepcopy(DEFAULT_COLTRANE_SETTINGS)
    coltrane_settings["SITE_URL"] = "http://localhost"

    return coltrane_settings


def pytest_configure():
    base_dir = Path(".")
    config = Config(base_dir=base_dir)

    templates = deepcopy(config.get_templates_settings())

    settings.configure(
        BASE_DIR=base_dir,
        SECRET_KEY="this-is-a-secret",
        TEMPLATES=templates,
        ROOT_URLCONF="coltrane.urls",
        INSTALLED_APPS=[
            "django.contrib.sitemaps",
            "django_fastdev.apps.FastDevConfig",
            "coltrane",
        ],
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            }
        },
        STATIC_ROOT=base_dir / "output" / "static",
        SETTINGS_MODULE="coltrane",
        COLTRANE=get_coltrane_settings(),
    )


@pytest.fixture(autouse=True)
def reset_settings(settings):
    # Set the settings
    settings.COLTRANE = get_coltrane_settings()
    reset_config_cache()

    # Run test
    yield
