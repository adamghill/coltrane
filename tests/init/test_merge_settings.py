from copy import deepcopy
from pathlib import Path
from unittest.mock import ANY, Mock, patch

from coltrane import _merge_settings
from tests.init.test_initialize import (  # type: ignore
    DEFAULT_SETTINGS,
    _get_settings,
)


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
def test_merge_settings_no_extras_with_args():
    expected = deepcopy(DEFAULT_SETTINGS)
    expected["INSTALLED_APPS"].append("django_browser_reload")
    expected["MIDDLEWARE"].append("django_browser_reload.middleware.BrowserReloadMiddleware")

    actual = _merge_settings(Path("."), {})

    # Remove the ENV key because it won't be set for this code path
    del expected["ENV"]

    assert actual == expected


@patch("coltrane.is_whitenoise_installed", Mock(return_value=True))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
def test_merge_settings_with_whitenoise():
    expected = _get_settings()

    expected.update(
        {
            "WHITENOISE_MANIFEST_STRICT": False,
            "STATICFILES_STORAGE": ANY,
        }
    )

    expected["INSTALLED_APPS"].insert(0, "whitenoise.runserver_nostatic")
    expected["MIDDLEWARE"].insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

    # Remove the ENV key because it won't be set for this code path
    del expected["ENV"]

    actual = _merge_settings(Path("."), {})

    assert actual == expected


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=True))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
def test_merge_settings_with_django_unicorn():
    actual = _merge_settings(Path("."), {})
    installed_apps = actual["INSTALLED_APPS"]

    assert "django_unicorn" in installed_apps
    assert "unicorn" not in installed_apps


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=True))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=True))
def test_merge_settings_with_django_unicorn_and_unicorn():
    actual = _merge_settings(Path("."), {})
    installed_apps = actual["INSTALLED_APPS"]

    assert "django_unicorn" in installed_apps
    assert "unicorn" in installed_apps


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
def test_merge_settings_no_django_unicorn():
    actual = _merge_settings(Path("."), {})
    installed_apps = actual["INSTALLED_APPS"]

    assert "django_unicorn" not in installed_apps
    assert "unicorn" not in installed_apps


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=True))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
def test_merge_settings_with_django_compressor():
    actual = _merge_settings(Path("."), {})

    assert "compressor" in actual["INSTALLED_APPS"]

    assert "COMPRESS_ENABLED" in actual
    assert actual["COMPRESS_ENABLED"]

    assert "STATICFILES_FINDERS" in actual

    assert "compressor.finders.CompressorFinder" in actual["STATICFILES_FINDERS"]
    assert "compressor.templatetags.compress" in actual["TEMPLATES"][0]["OPTIONS"]["builtins"]


@patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
@patch("coltrane.is_django_compressor_installed", Mock(return_value=True))
@patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
@patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
@patch("sys.argv", ["app.py", "compress"])
def test_merge_settings_with_django_compressor_compress_offline():
    actual = _merge_settings(Path("."), {})

    assert "COMPRESS_OFFLINE" in actual
    assert actual["COMPRESS_OFFLINE"] is True


# @patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
# @patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
# @patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
# @patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
# @patch("coltrane.is_dj_angles_installed", Mock(return_value=True))
# def test_merge_settings_with_dj_angles():
#     actual = _merge_settings(Path("."), {})
#     assert actual["TEMPLATES"]
#     template = actual["TEMPLATES"][0]

#     assert "APP_DIRS" not in template

#     assert template["OPTIONS"]["loaders"]
#     assert template["OPTIONS"]["loaders"][0] == "dj_angles.template_loader.Loader"


# @patch("coltrane.is_whitenoise_installed", Mock(return_value=False))
# @patch("coltrane.is_django_compressor_installed", Mock(return_value=False))
# @patch("coltrane.is_django_unicorn_installed", Mock(return_value=False))
# @patch("coltrane.is_unicorn_module_available", Mock(return_value=False))
# @patch("coltrane.is_dj_angles_installed", Mock(return_value=False))
# def test_merge_settings_no_dj_angles():
#     actual = _merge_settings(Path("."), {})
#     assert actual["TEMPLATES"]
#     template = actual["TEMPLATES"][0]

#     assert "APP_DIRS" in template
#     assert template["APP_DIRS"] is True

#     if "loaders" in template["OPTIONS"]:
#         assert "dj_angles.template_loader.Loader" not in template["OPTIONS"]["loaders"]
