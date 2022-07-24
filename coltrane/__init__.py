import logging
import sys
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
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django_fastdev",
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
    module_name = str(file)
    
    if str(base_dir) != ".":
        module_name = module_name.replace(str(base_dir), "")

    module_name = module_name.replace("/", ".")

    if module_name.startswith("."):
        module_name = module_name[1:]

    if module_name.endswith(".py"):
        module_name = module_name[:-3]
    else:
        raise InvalidTemplateLibrary()

    import_library(module_name)

    return module_name


def _get_default_template_settings(base_dir: Path) -> List:
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
                except InvalidTemplateLibrary as e:
                    logger.exception(e)

    builtins = [
        "django.contrib.humanize.templatetags.humanize",
        "django.templatetags.static",
        "coltrane.templatetags.coltrane_tags",
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
                    "django.template.context_processors.static",
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
    Retrieves environment value that could potentially be a list of strings.
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
    Merges the passed-in settings into the default `coltrane` settings.
    Passed-in settings will override the defaults.
    """

    # Assume that `argv[1] == "build"` means that the `build`
    # management command is currently being run
    is_build_management_command = len(sys.argv) >= 2 and sys.argv[1] == "build"

    debug = django_settings.get("DEBUG", getenv("DEBUG", "True") == "True")

    staticfiles_dirs = [
        base_dir / "static",
    ]

    middleware = deepcopy(DEFAULT_MIDDLEWARE_SETTINGS)
    installed_apps = deepcopy(DEFAULT_INSTALLED_APPS)

    is_whitenoise_installed = _is_whitenoise_installed()

    if is_whitenoise_installed:
        middleware.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
        installed_apps.insert(0, "whitenoise.runserver_nostatic")

    if debug and not is_build_management_command:
        # Add settings required for django-browser-reload when appropriate
        middleware.append("django_browser_reload.middleware.BrowserReloadMiddleware")
        installed_apps.append("django_browser_reload")

        # Add content and data to "staticfiles" so django-browser-reload will monitor
        staticfiles_dirs.append(base_dir / "content")
        staticfiles_dirs.append(base_dir / "data")

    default_settings = {
        "BASE_DIR": base_dir,
        "ROOT_URLCONF": "coltrane.urls",
        "DEBUG": debug,
        "SECRET_KEY": getenv("SECRET_KEY"),
        "INSTALLED_APPS": _merge_installed_apps(django_settings, installed_apps),
        "CACHES": DEFAULT_CACHES_SETTINGS,
        "MIDDLEWARE": middleware,
        "TEMPLATES": _get_default_template_settings(base_dir),
        "INTERNAL_IPS": _get_from_env("INTERNAL_IPS"),
        "ALLOWED_HOSTS": _get_from_env("ALLOWED_HOSTS"),
        "STATIC_ROOT": base_dir / "output" / "static",
        "STATIC_URL": "static/",
        "STATICFILES_DIRS": staticfiles_dirs,
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
        # Hard-coding `SETTINGS_MODULE` even though it kind of doesn't make sense, but
        # is needed for rendering a nice 500 page on local when debugging
        "SETTINGS_MODULE": "coltrane",
    }

    coltrane_site = getenv("COLTRANE_SITE")

    if coltrane_site:
        default_settings["COLTRANE"]["SITE"] = coltrane_site

    coltrane_title = getenv("COLTRANE_TITLE")

    if coltrane_title:
        default_settings["COLTRANE"]["TITLE"] = coltrane_title

    coltrane_description = getenv("COLTRANE_DESCRIPTION")

    if coltrane_description:
        default_settings["COLTRANE"]["DESCRIPTION"] = coltrane_description

    if is_whitenoise_installed:
        default_settings["WHITENOISE_MANIFEST_STRICT"] = False
        default_settings[
            "STATICFILES_STORAGE"
        ] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    # Make sure BASE_DIR is a `Path` if it got passed in
    if "BASE_DIR" in django_settings and isinstance(django_settings["BASE_DIR"], str):
        django_settings["BASE_DIR"] = Path(django_settings["BASE_DIR"])

    # Override STATIC_ROOT if the output directory name is manually set
    try:
        django_settings["STATIC_ROOT"] = (
            base_dir / django_settings["COLTRANE"]["OUTPUT"]["PATH"] / "static"
        )
    except KeyError:
        pass

    # Override STATIC_ROOT if the output directory is manually set
    try:
        django_settings["STATIC_ROOT"] = (
            Path(django_settings["COLTRANE"]["OUTPUT"]["DIRECTORY"]) / "static"
        )
    except KeyError:
        pass

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
    **django_settings: Dict[str, Any],
) -> WSGIHandler:
    """
    Initializes the Django static site.
    """

    base_dir = _get_base_dir(django_settings.get("BASE_DIR"))

    load_dotenv(base_dir / ".env")

    django_settings = _merge_settings(base_dir, django_settings)
    _configure_settings(django_settings)

    django_setup()

    return WSGIHandler()
