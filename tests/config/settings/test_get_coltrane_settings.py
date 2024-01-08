import pytest

from coltrane.config.settings import (
    DEFAULT_COLTRANE_SETTINGS,
    get_coltrane_settings,
    get_content_directory,
    get_data_directory,
    get_data_json_5,
    get_description,
    get_extra_file_names,
    get_markdown_renderer,
    get_site_url,
    get_title,
)


def test_get_coltrane_settings_none(settings):
    settings.COLTRANE = {}
    assert get_coltrane_settings() == {}


def test_get_coltrane_settings_default(settings):
    del settings.COLTRANE
    assert get_coltrane_settings() == DEFAULT_COLTRANE_SETTINGS


def test_get_coltrane_settings_invalid_type(settings):
    settings.COLTRANE = "str"

    with pytest.raises(TypeError):
        get_coltrane_settings()


def test_get_site_url(settings):
    settings.COLTRANE = {"SITE_URL": "http://test-site.com"}
    assert get_site_url() == "http://test-site.com"


def test_get_title(settings):
    settings.COLTRANE = {"TITLE": "test-title"}
    assert get_title() == "test-title"


def test_get_description(settings):
    settings.COLTRANE = {"DESCRIPTION": "test description"}
    assert get_description() == "test description"


def test_get_data_directory(settings):
    settings.COLTRANE = {"DATA_DIRECTORY": "test-data-directory"}
    assert get_data_directory() == "test-data-directory"


def test_data_directory_default():
    assert get_data_directory() == "data"


def test_content_directory(settings):
    settings.COLTRANE = {"CONTENT_DIRECTORY": "test-content-directory"}
    assert get_content_directory() == "test-content-directory"


def test_content_directory_default():
    assert get_content_directory() == "content"


def test_get_markdown_renderer(settings):
    assert get_markdown_renderer() == "mistune"

    settings.COLTRANE = {"MARKDOWN_RENDERER": "invalid-markdown-renderer"}

    with pytest.raises(AssertionError):
        get_markdown_renderer()


def test_get_extra_file_names(settings):
    settings.COLTRANE = {"EXTRA_FILE_NAMES": ["robots.txt"]}
    assert get_extra_file_names() == ["robots.txt"]


def test_get_data_json_5(settings):
    assert get_data_json_5() is False

    settings.COLTRANE = {"DATA_JSON5": True}
    assert get_data_json_5() is True
