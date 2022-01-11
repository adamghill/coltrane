import logging
from os import getenv
from pathlib import Path
from typing import Any, Dict, List, Optional

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.template.library import InvalidTemplateLibrary, import_library
from django.urls import include, path

from dotenv import load_dotenv

from coltrane.config.settings import DEFAULT_COLTRANE_SETTINGS

from .utils import dict_merge


logger = logging.getLogger(__name__)

__all__ = [
    "initialize",
]


urlpatterns = [
    path("", include("coltrane.urls")),
]

DEFAULT_CACHES_SETTINGS = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

DEFAULT_MIDDLEWARE_SETTINGS = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DEFAULT_INSTALLED_APPS = [
    "django.contrib.humanize",
    "coltrane",
]


def _get_base_dir(base_dir: Optional[Path]) -> Path:
    if base_dir is None:
        base_dir = Path(".")
    elif isinstance(base_dir, str):
        base_dir = Path(base_dir)

    return base_dir


def _get_template_tag_module_name(base_dir: Path, file: Path) -> str:
    """
    Get a dot notation module name if a particular file path is a template tag.
    """

    # TODO: Cleaner way to convert a string path to a module dot notation?
    module_name = str(file).replace(str(base_dir), "")
    module_name = module_name.replace("/", ".")

    if module_name.startswith("."):
        module_name = module_name[1:]

    if module_name.endswith(".py"):
        module_name = module_name[:-3]

    import_library(module_name)
    return module_name


def _get_default_template_settings(base_dir: Path):
    """
    Gets default template settings, including templates and built-in template tags.
    """

    template_dir = base_dir / "templates"
    templatetags_dir = base_dir / "templatetags"
    template_tags = []

    if templatetags_dir.exists():
        for template_tag_path in templatetags_dir.rglob("*.py"):
            if template_tag_path.is_file():
                try:
                    module_name = _get_template_tag_module_name(
                        base_dir, template_tag_path
                    )
                    template_tags.append(module_name)
                except InvalidTemplateLibrary:
                    pass

    builtins = [
        "django.contrib.humanize.templatetags.humanize",
    ]
    builtins.extend(template_tags)

    return [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "DIRS": [template_dir],
            "OPTIONS": {
                "builtins": builtins,
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.template.context_processors.debug",
                ],
            },
        }
    ]


def _merge_installed_apps(django_settings: Dict[str, Any]) -> List[str]:
    """
    Gets the installed apps from the passed-in settings and adds `coltrane` to it.
    """

    installed_apps = list(django_settings.get("INSTALLED_APPS", []))
    installed_apps.extend(DEFAULT_INSTALLED_APPS)

    return installed_apps


def _merge_settings(base_dir: Path, django_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merges the passed-in settings into the default `coltrane` settings. Passed-in settings will override the defaults.
    """

    internal_ips = []

    if internal_ips_from_env := getenv("INTERNAL_IPS"):
        internal_ips = internal_ips_from_env.split(",")

    default_settings = {
        "BASE_DIR": base_dir,
        "ROOT_URLCONF": __name__,
        "DEBUG": getenv("DEBUG", "True") == "True",
        "SECRET_KEY": getenv("SECRET_KEY"),
        "INSTALLED_APPS": _merge_installed_apps(django_settings),
        "CACHES": DEFAULT_CACHES_SETTINGS,
        "MIDDLWARE": DEFAULT_MIDDLEWARE_SETTINGS,
        "TEMPLATES": _get_default_template_settings(base_dir),
        "INTERNAL_IPS": internal_ips,
        "COLTRANE": DEFAULT_COLTRANE_SETTINGS,
    }

    django_settings = dict_merge(
        default_settings, django_settings, destination_overrides_source=True
    )
    logger.debug(f"Merged settings: {django_settings}")

    return django_settings


def _configure_settings(django_settings: Dict[str, Any]) -> None:
    """
    Configures the settings in Django.
    """

    settings.configure(**django_settings)


def initialize(
    base_dir: Optional[Path] = None,
    **django_settings: Dict[str, Any],
) -> WSGIHandler:
    """
    Initializes the Django static site.
    """

    base_dir = _get_base_dir(base_dir)

    load_dotenv(base_dir / ".env")

    django_settings = _merge_settings(base_dir, django_settings)
    _configure_settings(django_settings)

    return WSGIHandler()
