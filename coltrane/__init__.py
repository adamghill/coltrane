import logging
from copy import deepcopy
from os import getenv
from pathlib import Path
from typing import Any, Dict, List, Optional

from django import setup as django_setup
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.template.library import InvalidTemplateLibrary, import_library

from dotenv import load_dotenv

from coltrane.config.settings import DEFAULT_COLTRANE_SETTINGS

from .utils import dict_merge


logger = logging.getLogger(__name__)

__all__ = [
    "initialize",
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
    "django.contrib.staticfiles",
    "coltrane",
]


def _get_base_dir(base_dir: Optional[Path]) -> Path:
    """
    Gets the base directory.
    """

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
    else:
        raise InvalidTemplateLibrary()

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
        "django.templatetags.static",
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


def _merge_installed_apps(
    django_settings: Dict[str, Any], installed_apps: List[str]
) -> List[str]:
    """
    Gets the installed apps from the passed-in settings and adds `coltrane` to it.
    """

    if "INSTALLED_APPS" in django_settings:
        installed_apps.extend(list(django_settings["INSTALLED_APPS"]))

    return installed_apps


def _get_from_env(env_name: str) -> List[str]:
    """
    Retrieves environment value that could potentially be an list of strings.
    """

    env_values = []

    if value_from_env := getenv(env_name):
        env_values = value_from_env.split(",")

    return env_values


def _is_whitenoise_installed() -> bool:
    """
    Helper function to check if `whitenoise` is installed.
    """

    try:
        import whitenoise

        return True
    except ModuleNotFoundError:
        pass

    return False


def _merge_settings(base_dir: Path, django_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merges the passed-in settings into the default `coltrane` settings. Passed-in settings will override the defaults.
    """

    is_whitenoise_installed = _is_whitenoise_installed()

    middleware = deepcopy(DEFAULT_MIDDLEWARE_SETTINGS)
    installed_apps = deepcopy(DEFAULT_INSTALLED_APPS)

    if is_whitenoise_installed:
        middleware.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        installed_apps.insert(len(installed_apps) - 1, "whitenoise.runserver_nostatic")

    default_settings = {
        "BASE_DIR": base_dir,
        "ROOT_URLCONF": "coltrane.urls",
        "DEBUG": getenv("DEBUG", "True") == "True",
        "SECRET_KEY": getenv("SECRET_KEY"),
        "INSTALLED_APPS": _merge_installed_apps(django_settings, installed_apps),
        "CACHES": DEFAULT_CACHES_SETTINGS,
        "MIDDLEWARE": middleware,
        "TEMPLATES": _get_default_template_settings(base_dir),
        "INTERNAL_IPS": _get_from_env("INTERNAL_IPS"),
        "ALLOWED_HOSTS": _get_from_env("ALLOWED_HOSTS"),
        "STATIC_ROOT": base_dir / "output" / "static",
        "STATIC_URL": "static/",
        "STATICFILES_DIRS": [
            base_dir / "static",
        ],
        "LOGGING": {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": "ERROR",
            },
        },
        "COLTRANE": DEFAULT_COLTRANE_SETTINGS,
    }

    if is_whitenoise_installed:
        default_settings["WHITENOISE_MANIFEST_STRICT"] = False
        default_settings[
            "STATICFILES_STORAGE"
        ] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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

    django_setup()

    return WSGIHandler()
