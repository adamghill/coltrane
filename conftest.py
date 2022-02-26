from copy import deepcopy
from pathlib import Path

from django.conf import settings

from coltrane import _get_default_template_settings


def pytest_configure():
    base_dir = Path(".")

    templates = deepcopy(_get_default_template_settings(base_dir))

    settings.configure(
        BASE_DIR=base_dir,
        SECRET_KEY="this-is-a-secret",
        TEMPLATES=templates,
        ROOT_URLCONF="coltrane.urls",
        INSTALLED_APPS=[
            "django_fastdev.django_app.FastDevConfig",
            "coltrane",
        ],
        CACHES={
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            }
        },
        STATIC_ROOT=base_dir / "output" / "static",
        SETTINGS_MODULE="coltrane",
    )
