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
    # _get_default_template_settings,
    initialize,
)
from coltrane.config.settings import get_config

base_dir = Path(".")
config = get_config()

DEFAULT_SETTINGS = {
    "BASE_DIR": base_dir,
    "ROOT_URLCONF": "coltrane.urls",
    "DEBUG": True,
    "SECRET_KEY": ANY,
    "INSTALLED_APPS": deepcopy(DEFAULT_INSTALLED_APPS),
    "CACHES": deepcopy(DEFAULT_CACHES_SETTINGS),
    "MIDDLEWARE": deepcopy(DEFAULT_MIDDLEWARE),
    "TEMPLATES": deepcopy(config.get_templates_settings()),
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
@patch(
    "coltrane.config.coltrane.configurators.templates.TemplatesConfigurator._get_template_tag_module_name",
    Mock(return_value="fake.templatetag"),
)
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
@patch(
    "coltrane.config.coltrane.configurators.templates.TemplatesConfigurator._get_template_tag_module_name",
    Mock(side_effect=InvalidTemplateLibrary),
)
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
@patch(
    "coltrane.config.coltrane.configurators.templates.TemplatesConfigurator._get_template_tag_module_name",
    Mock(return_value="fake.templatetag"),
)
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
    expected["STATICFILES_DIRS"] = expected["STATICFILES_DIRS"] = [tmp_path]

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
    expected["STATICFILES_DIRS"] = [tmp_path]

    _configure_settings.assert_called_once_with(expected)


"""
{
    'BASE_DIR': PosixPath('/private/var/folders/4_/41j53rw1683_y0qzt18qrn4r0000gn/T/pytest-of-adam/pytest-956/test_staticfiles_dirs_data0'),
    'ROOT_URLCONF': 'coltrane.urls',
    'DEBUG': True,
    'SECRET_KEY': <ANY>,
    'INSTALLED_APPS': ['django.contrib.humanize', 'django.contrib.sitemaps', 'django.contrib.staticfiles', 'django_fastdev', 'coltrane', 'django_browser_reload'],
    'CACHES': {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        }
    },
    'MIDDLEWARE': ['coltrane.middleware.IsSecureMiddleware', 'django.middleware.security.SecurityMiddleware', 'django.middleware.gzip.GZipMiddleware', 'django.middleware.http.ConditionalGetMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware', 'django_browser_reload.middleware.BrowserReloadMiddleware'],
    'TEMPLATES': <ANY>,
    'INTERNAL_IPS': [],
    'ALLOWED_HOSTS': [],
    'STATIC_ROOT': <ANY>,
    'STATIC_URL': <ANY>,
    'STATICFILES_DIRS': [PosixPath('/private/var/folders/4_/41j53rw1683_y0qzt18qrn4r0000gn/T/pytest-of-adam/pytest-956/test_staticfiles_dirs_data0/static'), PosixPath('/private/var/folders/4_/41j53rw1683_y0qzt18qrn4r0000gn/T/pytest-of-adam/pytest-956/test_staticfiles_dirs_data0/data')],
    'TIME_ZONE': <ANY>,
    'LOGGING': <ANY>,
    'COLTRANE': {
        'TITLE': '',
        'DESCRIPTION': '',
        'SITE_URL': '',
        'MARKDOWN_RENDERER': 'mistune',
        'MISTUNE_PLUGINS': ['strikethrough', 'footnotes', 'table', 'task_lists', 'def_list', 'abbr', 'mark', 'insert', 'superscript', 'subscript'],
        'EXTRA_FILE_NAMES': [],
        'CONTENT_DIRECTORY': 'content',
        'DATA_DIRECTORY': 'data',
        'DISABLE_WILDCARD_TEMPLATES': False,
        'IS_SECURE': False,
        'DATA_JSON5': False,
        'SITES': {}
    },
    'SETTINGS_MODULE': 'coltrane',
    'ENV': <ANY>
}
"""

"""
{
  "BASE_DIR": "/private/var/folders/4_/41j53rw1683_y0qzt18qrn4r0000gn/T/pytest-of-adam/pytest-956/test_staticfiles_dirs_data0",
  "ROOT_URLCONF": "coltrane.urls",
  "DEBUG": true,
  "SECRET_KEY": null,
  "INSTALLED_APPS": [
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django_fastdev",
    "coltrane",
    "django_browser_reload"
  ],
  "CACHES": {
    "default": {
      "BACKEND": "django.core.cache.backends.dummy.DummyCache"
    }
  },
  "MIDDLEWARE": [
    "coltrane.middleware.IsSecureMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware"
  ],
  "TEMPLATES": [
    {
      "BACKEND": "django.template.backends.django.DjangoTemplates",
      "DIRS": [
        "/private/var/folders/4_/41j53rw1683_y0qzt18qrn4r0000gn/T/pytest-of-adam/pytest-956/test_staticfiles_dirs_data0/templates"
      ],
      "OPTIONS": {
        "builtins": [
          "django.contrib.humanize.templatetags.humanize",
          "django.templatetags.static",
          "coltrane.templatetags.coltrane_tags"
        ],
        "context_processors": [
          "django.template.context_processors.request",
          "django.template.context_processors.debug",
          "django.template.context_processors.static",
          "coltrane.context_processors.coltrane"
        ],
        "loaders": [
          [
            "django.template.loaders.cached.Loader",
            [
              "dj_angles.template_loader.Loader",
              "django.template.loaders.filesystem.Loader",
              "django.template.loaders.app_directories.Loader"
            ]
          ]
        ]
      }
    }
  ],
  "INTERNAL_IPS": [],
  "ALLOWED_HOSTS": [],
  "STATIC_ROOT": "/private/var/folders/4_/41j53rw1683_y0qzt18qrn4r0000gn/T/pytest-of-adam/pytest-956/test_staticfiles_dirs_data0/output/static",
  "STATIC_URL": "static/",
  "STATICFILES_DIRS": [
    "/private/var/folders/4_/41j53rw1683_y0qzt18qrn4r0000gn/T/pytest-of-adam/pytest-956/test_staticfiles_dirs_data0"
  ],
  "TIME_ZONE": "UTC",
  "LOGGING": {
    "version": 1,
    "disable_existing_loggers": false,
    "handlers": {
      "console": {
        "class": "logging.StreamHandler"
      }
    },
    "root": {
      "handlers": ["console"],
      "level": "ERROR"
    }
  },
  "COLTRANE": {
    "TITLE": "",
    "DESCRIPTION": "",
    "SITE_URL": "",
    "MARKDOWN_RENDERER": "mistune",
    "MISTUNE_PLUGINS": [
      "strikethrough",
      "footnotes",
      "table",
      "task_lists",
      "def_list",
      "abbr",
      "mark",
      "insert",
      "superscript",
      "subscript"
    ],
    "EXTRA_FILE_NAMES": [],
    "CONTENT_DIRECTORY": "content",
    "DATA_DIRECTORY": "data",
    "DISABLE_WILDCARD_TEMPLATES": false,
    "IS_SECURE": false,
    "DATA_JSON5": false,
    "SITES": {}
  },
  "SETTINGS_MODULE": "coltrane",
  "ENV": {
    "ARGS": "tests/init/test_initialize.py::test_staticfiles_dirs_data",
    "ASDF_DIR": "/Users/adam/.asdf",
    "COLORTERM": "truecolor",
    "COMMAND_MODE": "unix2003",
    "GHOSTTY_BIN_DIR": "/Applications/Ghostty.app/Contents/MacOS",
    "GHOSTTY_RESOURCES_DIR": "/Applications/Ghostty.app/Contents/Resources/ghostty",
    "GHOSTTY_SHELL_INTEGRATION_NO_SUDO": "1",
    "HEX": "0123456789abcdef",
    "HEXLOWER": "0123456789abcdef",
    "HEXUPPER": "0123456789ABCDEF",
    "HOME": "/Users/adam",
    "HOMEBREW_CELLAR": "/opt/homebrew/Cellar",
    "HOMEBREW_PREFIX": "/opt/homebrew",
    "HOMEBREW_REPOSITORY": "/opt/homebrew",
    "INFOPATH": "/opt/homebrew/share/info",
    "LANG": "en_US.UTF-8",
    "LOGNAME": "adam",
    "MANPATH": ":/usr/share/man:/usr/local/share/man::/Applications/Ghostty.app/Contents/Resources/ghostty/../man",
    "NIX_PROFILES": "/nix/var/nix/profiles/default /Users/adam/.nix-profile",
    "NIX_SSL_CERT_FILE": "/nix/var/nix/profiles/default/etc/ssl/certs/ca-bundle.crt",
    "NVM_BIN": "/Users/adam/.nvm/versions/node/v7.2.1/bin/node",
    "PATH": "/Users/adam/Source/adamghill/coltrane/.venv/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/adam/.nvm/versions/node/v7.2.1/bin:/Users/adam/.asdf/shims:/Users/adam/.asdf/bin:/Users/adam/.pyenv/shims:/Users/adam/.cargo/bin:/Users/adam/.nix-profile/bin:/nix/var/nix/profiles/default/bin:/Users/adam/.codeium/windsurf/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Library/Apple/usr/bin:/usr/local/go/bin:/Applications/Ghostty.app/Contents/MacOS:/Users/adam/.local/bin",
    "PWD": "/Users/adam/Source/adamghill/coltrane",
    "PYENV_ROOT": "/Users/adam/.pyenv",
    "PYENV_SHELL": "fish",
    "PYTHONDONTWRITEBYTECODE": "1",
    "SHELL": "/opt/homebrew/bin/fish",
    "SHLVL": "2",
    "SSH_AUTH_SOCK": "/private/tmp/com.apple.launchd.opfPALd2Y5/Listeners",
    "STARSHIP_SESSION_KEY": "2439117425178122",
    "STARSHIP_SHELL": "fish",
    "TERM": "xterm-ghostty",
    "TERMINFO": "/Applications/Ghostty.app/Contents/Resources/terminfo",
    "TERM_PROGRAM": "ghostty",
    "TERM_PROGRAM_VERSION": "1.0.0",
    "TMPDIR": "/var/folders/4_/41j53rw1683_y0qzt18qrn4r0000gn/T/",
    "USER": "adam",
    "VIRTUAL_ENV": "/Users/adam/Source/adamghill/coltrane/.venv",
    "XDG_DATA_DIRS": "/usr/local/share:/usr/share:/Applications/Ghostty.app/Contents/Resources/ghostty/..",
    "XPC_FLAGS": "0x0",
    "XPC_SERVICE_NAME": "0",
    "_": "/Users/adam/.cargo/bin/uv",
    "__CFBundleIdentifier": "com.mitchellh.ghostty",
    "__CF_USER_TEXT_ENCODING": "0x1F5:0x0:0x0",
    "src": "coltrane",
    "PYTEST_VERSION": "8.3.3",
    "PYTEST_CURRENT_TEST": "tests/init/test_initialize.py::test_staticfiles_dirs_data (call)"
  }
}
"""
