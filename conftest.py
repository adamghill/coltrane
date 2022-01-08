from pathlib import Path

from django.conf import settings

from coltrane import DEFAULT_TEMPLATES_SETTINGS


def pytest_configure():
    settings.configure(
        BASE_DIR=Path("."),
        SECRET_KEY="this-is-a-secret",
        TEMPLATES=DEFAULT_TEMPLATES_SETTINGS,
        ROOT_URLCONF="coltrane.urls",
        INSTALLED_APPS=[
            "coltrane",
        ],
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            }
        },
    )
