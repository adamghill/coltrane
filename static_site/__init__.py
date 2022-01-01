from os import getenv
from pathlib import Path
from typing import Any, Dict, List, Optional

from django.conf import settings
from django.urls import include, path
from dotenv import load_dotenv

urlpatterns = [
    path("", include("static_site.urls")),
]


def initialize(
    base_dir: Path = Path("."),
    installed_apps: Optional[List] = None,
    allowed_hosts: Optional[List] = None,
    **extra_settings: Dict[str, Any]
) -> None:
    """
    Initializes the Django static site.
    """

    load_dotenv(base_dir)

    if installed_apps is None:
        installed_apps = []

    settings_installed_apps = installed_apps + [
        "static_site",
    ]

    # TODO: Should extra_settings be merged into the defaults instead of tacked onto the end?

    settings.configure(
        BASE_DIR=base_dir,
        ROOT_URLCONF=__name__,
        DEBUG=getenv("DEBUG", "True") == "True",
        SECRET_KEY=getenv("SECRET_KEY"),
        INSTALLED_APPS=settings_installed_apps,
        ALLOWED_HOSTS=allowed_hosts,
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
            },
        ],
        **extra_settings
    )
