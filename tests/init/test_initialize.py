from copy import deepcopy
from os import environ
from pathlib import Path
from unittest.mock import ANY, Mock, patch

from django.template.library import InvalidTemplateLibrary

from coltrane import (
    DEFAULT_CACHES_SETTINGS,
    DEFAULT_COLTRANE_SETTINGS,
    DEFAULT_INSTALLED_APPS,
    DEFAULT_MIDDLEWARE,
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
    "MIDDLEWARE": deepcopy(DEFAULT_MIDDLEWARE),
    "TEMPLATES": deepcopy(_get_default_template_settings(base_dir)),
    "INTERNAL_IPS": [],
    "ALLOWED_HOSTS": [],
    "STATIC_ROOT": ANY,
    "STATIC_URL": ANY,
    "STATICFILES_DIRS": ANY,
    "TIME_ZONE": ANY,
    "LOGGING": ANY,
    "COLTRANE": deepcopy(DEFAULT_COLTRANE_SETTINGS),
    "SETTINGS_MODULE": "coltrane",
    "ENV": ANY,
}


def _get_settings():
    settings = deepcopy(DEFAULT_SETTINGS)

    settings["INSTALLED_APPS"].append("django_browser_reload")
    settings["MIDDLEWARE"].append("django_browser_reload.middleware.BrowserReloadMiddleware")

    return settings


def _get_settings_with_debug_false():
    settings = deepcopy(DEFAULT_SETTINGS)
    settings["DEBUG"] = False

    return settings


@patch("coltrane.is_whitenoise_installed", return_value=False)
@patch("coltrane.is_django_compressor_installed", return_value=False)
@patch("coltrane.is_django_unicorn_installed", return_value=False)
@patch("coltrane.is_unicorn_module_available", return_value=False)
@patch("coltrane._configure_settings")
def test_no_base_dir(_configure_settings, *args):
    initialize()

    expected = _get_settings()

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", return_value=False)
@patch("coltrane.is_django_compressor_installed", return_value=False)
@patch("coltrane.is_django_unicorn_installed", return_value=False)
@patch("coltrane.is_unicorn_module_available", return_value=False)
@patch("coltrane._configure_settings")
def test_with_base_dir(_configure_settings, *args):
    initialize(BASE_DIR=Path("test"))

    expected = _get_settings()
    expected["BASE_DIR"] = Path("test")
    expected["TEMPLATES"][0]["DIRS"] = [Path("test") / "templates"]

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", return_value=False)
@patch("coltrane.is_django_compressor_installed", return_value=False)
@patch("coltrane.is_django_unicorn_installed", return_value=False)
@patch("coltrane.is_unicorn_module_available", return_value=False)
@patch("coltrane._configure_settings")
def test_with_base_dir_as_string(_configure_settings, *args):
    initialize(BASE_DIR="test")

    expected = _get_settings()
    expected["BASE_DIR"] = Path("test")
    expected["TEMPLATES"][0]["DIRS"] = [Path("test") / "templates"]

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane._get_template_tag_module_name", Mock(return_value="fake.templatetag"))
@patch("coltrane._configure_settings")
def test_with_template_tags(_configure_settings, tmp_path):
    (tmp_path / "templatetags").mkdir()
    # not actually used, but need the file here
    (tmp_path / "templatetags" / "sample_tag.py").touch()

    initialize(BASE_DIR=tmp_path)

    expected = _get_settings()
    expected["BASE_DIR"] = ANY
    expected["TEMPLATES"][0]["DIRS"] = ANY
    expected["TEMPLATES"][0]["OPTIONS"]["builtins"].append("fake.templatetag")

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane._get_template_tag_module_name", Mock(side_effect=InvalidTemplateLibrary))
@patch("coltrane._configure_settings")
def test_with_invalid_template_tag(_configure_settings, tmp_path):
    (tmp_path / "templatetags").mkdir()
    # not actually used, but need the file here
    (tmp_path / "templatetags" / "sample_tag.py").touch()

    initialize(BASE_DIR=tmp_path)

    expected = _get_settings()
    expected["BASE_DIR"] = ANY
    expected["TEMPLATES"][0]["DIRS"] = ANY

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane._get_template_tag_module_name", Mock(return_value="fake.templatetag"))
@patch("coltrane._configure_settings")
def test_with_template_tags_in_directory_with_py_extension(_configure_settings, tmp_path):
    (tmp_path / "templatetags").mkdir()
    (tmp_path / "templatetags" / "sample.py").mkdir()
    # not actually used, but need the file here
    (tmp_path / "templatetags" / "sample.py" / "sample_tag.py").touch()

    initialize(BASE_DIR=tmp_path)

    expected = _get_settings()
    expected["BASE_DIR"] = ANY
    expected["TEMPLATES"][0]["DIRS"] = ANY
    expected["TEMPLATES"][0]["OPTIONS"]["builtins"].append("fake.templatetag")

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane.is_dj_angles_installed", Mock(return_value=False))
@patch("coltrane._configure_settings")
def test_debug_setting(_configure_settings):
    initialize(DEBUG=False)

    expected = _get_settings_with_debug_false()
    expected["TEMPLATES"] = ANY

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane.is_dj_angles_installed", Mock(return_value=False))
@patch.dict(environ, {"DEBUG": "False"})
@patch("coltrane._configure_settings")
def test_debug_env(_configure_settings):
    initialize()

    expected = _get_settings_with_debug_false()
    expected["TEMPLATES"] = ANY

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane._configure_settings")
def test_time_zone_default(_configure_settings):
    initialize()

    expected = _get_settings()
    expected["TIME_ZONE"] = "UTC"

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane._configure_settings")
def test_time_zone_setting(_configure_settings):
    initialize(TIME_ZONE="America/New_York")

    expected = _get_settings()
    expected["TIME_ZONE"] = "America/New_York"

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch.dict(environ, {"TIME_ZONE": "America/Chicago"})
@patch("coltrane._configure_settings")
def test_time_zone_env(_configure_settings):
    initialize()

    expected = _get_settings()
    expected["TIME_ZONE"] = "America/Chicago"

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane._configure_settings")
def test_staticfiles_dirs(_configure_settings):
    initialize()

    expected = _get_settings()
    expected["STATICFILES_DIRS"] = [Path("static")]

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane._configure_settings")
def test_staticfiles_dirs_content(_configure_settings, tmp_path: Path):
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test.txt").write_text("test")

    initialize(BASE_DIR=tmp_path)

    expected = _get_settings()
    expected["BASE_DIR"] = tmp_path
    expected["TEMPLATES"] = ANY
    expected["STATICFILES_DIRS"] = [tmp_path / "static", tmp_path / "content"]

    _configure_settings.assert_called_once_with(expected)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("coltrane._configure_settings")
def test_staticfiles_dirs_data(_configure_settings, tmp_path: Path):
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.json").write_text("{}")

    initialize(BASE_DIR=tmp_path)

    expected = _get_settings()
    expected["BASE_DIR"] = tmp_path
    expected["TEMPLATES"] = ANY
    expected["STATICFILES_DIRS"] = [tmp_path / "static", tmp_path / "data"]

    _configure_settings.assert_called_once_with(expected)
