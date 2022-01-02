import logging
from os import getenv
from pathlib import Path
from typing import Any, Dict, List, Optional

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.urls import include, path

from dotenv import load_dotenv

from .utils import dict_merge


logger = logging.getLogger(__name__)


urlpatterns = [
    path("", include("coltrane.urls")),
]


def _get_installed_apps(django_settings: Dict[str, Any]) -> List[str]:
    installed_apps = django_settings.get("INSTALLED_APPS", [])
    installed_apps.append("coltrane")

    return installed_apps


def initialize(
    base_dir: Optional[Path] = None,
    **django_settings: Dict[str, Any],
) -> WSGIHandler:
    """
    Initializes the Django static site.
    """

    if base_dir is None:
        base_dir = Path(".")

    load_dotenv(base_dir / ".env")

    caches = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

    middleware = [
        "django.middleware.security.SecurityMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    default_settings = {
        "BASE_DIR": base_dir,
        "ROOT_URLCONF": __name__,
        "DEBUG": getenv("DEBUG", "True") == "True",
        "SECRET_KEY": getenv("SECRET_KEY"),
        "INSTALLED_APPS": _get_installed_apps(django_settings),
        "CACHES": caches,
        "MIDDLWARE": middleware,
        "TEMPLATES": [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
            },
        ],
        "COLTRAN": {"VIEW_CACHE_SECONDS": 60 * 60},
    }

    django_settings = dict_merge(
        default_settings, django_settings, destination_overrides_source=True
    )
    logger.debug(f"Merged settings: {django_settings}")

    settings.configure(**django_settings)

    return WSGIHandler()
