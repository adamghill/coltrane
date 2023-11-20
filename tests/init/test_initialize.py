from copy import deepcopy
from pathlib import Path
from unittest.mock import ANY, patch

from django.template.library import InvalidTemplateLibrary

from coltrane import (
    DEFAULT_CACHES_SETTINGS,
    DEFAULT_COLTRANE_SETTINGS,
    DEFAULT_INSTALLED_APPS,
    DEFAULT_MIDDLEWARE_SETTINGS,
    _get_default_template_settings,
    initialize,
)

base_dir = Path(".")

DEFAULT_SETTINGS = {
    "BASE_DIR": base_dir,
    "ROOT_URLCONF": "coltrane.urls",
    "DEBUG": True,
    "SECRET_KEY": ANY,
    "INSTALLED_APPS": deepcopy(DEFAULT_INSTALLED_APPS),
    "CACHES": deepcopy(DEFAULT_CACHES_SETTINGS),
    "MIDDLEWARE": deepcopy(DEFAULT_MIDDLEWARE_SETTINGS),
    "TEMPLATES": deepcopy(_get_default_template_settings(base_dir)),
    "INTERNAL_IPS": [],
    "ALLOWED_HOSTS": [],
    "STATIC_ROOT": ANY,
    "STATIC_URL": ANY,
    "STATICFILES_DIRS": ANY,
    "LOGGING": ANY,
    "COLTRANE": deepcopy(DEFAULT_COLTRANE_SETTINGS),
    "SETTINGS_MODULE": "coltrane",
}


def _get_settings_with_whitenoise():
    settings = deepcopy(DEFAULT_SETTINGS)
    settings.update(
        {
            "WHITENOISE_MANIFEST_STRICT": False,
            "STATICFILES_STORAGE": ANY,
        }
    )

    settings["INSTALLED_APPS"] = deepcopy(DEFAULT_INSTALLED_APPS)
    settings["INSTALLED_APPS"].insert(0, "whitenoise.runserver_nostatic")

    settings["MIDDLEWARE"] = deepcopy(DEFAULT_MIDDLEWARE_SETTINGS)
    settings["MIDDLEWARE"].insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    settings["INSTALLED_APPS"].append("django_browser_reload")
    settings["MIDDLEWARE"].append(
        "django_browser_reload.middleware.BrowserReloadMiddleware"
    )

    return settings


@patch("coltrane._configure_settings")
# @patch("coltrane._is_whitenoise_installed", return_value=False)
def test_initialize_no_base_dir(_configure_settings):
    initialize()

    expected = _get_settings_with_whitenoise()

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane._configure_settings")
# @patch("coltrane._is_whitenoise_installed", return_value=False)
def test_initialize_with_base_dir(_configure_settings):
    initialize(BASE_DIR=Path("test"))

    expected = _get_settings_with_whitenoise()
    expected["BASE_DIR"] = Path("test")
    expected["TEMPLATES"][0]["DIRS"] = [Path("test") / "templates"]

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane._configure_settings")
def test_initialize_with_base_dir_as_string(_configure_settings):
    initialize(BASE_DIR="test")

    expected = _get_settings_with_whitenoise()
    expected["BASE_DIR"] = Path("test")
    expected["TEMPLATES"][0]["DIRS"] = [Path("test") / "templates"]

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane._configure_settings")
@patch("coltrane._get_template_tag_module_name", return_value="fake.templatetag")
def test_initialize_with_template_tags(
    _get_template_tag_module_name, _configure_settings, tmp_path
):
    (tmp_path / "templatetags").mkdir()
    # not actually used, but need the file here
    (tmp_path / "templatetags" / "sample_tag.py").touch()

    initialize(BASE_DIR=tmp_path)

    expected = _get_settings_with_whitenoise()
    expected["BASE_DIR"] = ANY
    expected["TEMPLATES"][0]["DIRS"] = ANY
    expected["TEMPLATES"][0]["OPTIONS"]["builtins"].append("fake.templatetag")

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane._configure_settings")
@patch("coltrane._get_template_tag_module_name", side_effect=InvalidTemplateLibrary)
def test_initialize_with_invalid_template_tag(
    _get_template_tag_module_name, _configure_settings, tmp_path
):
    (tmp_path / "templatetags").mkdir()
    # not actually used, but need the file here
    (tmp_path / "templatetags" / "sample_tag.py").touch()

    initialize(BASE_DIR=tmp_path)

    expected = _get_settings_with_whitenoise()
    expected["BASE_DIR"] = ANY
    expected["TEMPLATES"][0]["DIRS"] = ANY

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane._configure_settings")
@patch("coltrane._get_template_tag_module_name", return_value="fake.templatetag")
def test_initialize_with_template_tags_in_directory_with_py_extension(
    _get_template_tag_module_name, _configure_settings, tmp_path
):
    (tmp_path / "templatetags").mkdir()
    (tmp_path / "templatetags" / "sample.py").mkdir()
    # not actually used, but need the file here
    (tmp_path / "templatetags" / "sample.py" / "sample_tag.py").touch()

    initialize(BASE_DIR=tmp_path)

    expected = _get_settings_with_whitenoise()
    expected["BASE_DIR"] = ANY
    expected["TEMPLATES"][0]["DIRS"] = ANY
    expected["TEMPLATES"][0]["OPTIONS"]["builtins"].append("fake.templatetag")

    _configure_settings.assert_called_once_with(expected)
