from pathlib import Path

from django.conf import settings

from coltrane import _get_default_template_settings


def pytest_configure():
    base_dir = Path(".")

    settings.configure(
        BASE_DIR=base_dir,
        SECRET_KEY="this-is-a-secret",
        TEMPLATES=_get_default_template_settings(base_dir),
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
