from pathlib import Path

from django.conf import settings


def pytest_configure():
    templates = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
        }
    ]

    installed_apps = [
        "coltrane",
    ]

    # caches = {
    #     "default": {
    #         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    #         "LOCATION": "unique-snowflake",
    #     }
    # }

    settings.configure(
        BASE_DIR=Path("."),
        SECRET_KEY="this-is-a-secret",
        TEMPLATES=templates,
        ROOT_URLCONF="coltrane.urls",
        INSTALLED_APPS=installed_apps,
        # CACHES=caches,
    )
