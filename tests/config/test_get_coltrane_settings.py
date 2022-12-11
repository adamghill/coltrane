import pytest

from coltrane.config.settings import (
    DEFAULT_COLTRANE_SETTINGS,
    get_coltrane_settings,
    get_description,
    get_markdown_renderer,
    get_site_url,
    get_title,
)


def test_get_coltrane_settings_none(settings):
    setattr(settings, "COLTRANE", {})
    assert get_coltrane_settings() == {}


def test_get_coltrane_settings_default(settings):
    del settings.COLTRANE
    assert get_coltrane_settings() == DEFAULT_COLTRANE_SETTINGS


def test_get_coltrane_settings_invalid_type(settings):
    setattr(settings, "COLTRANE", "str")

    with pytest.raises(AssertionError):
        get_coltrane_settings()


def test_get_site_url(settings):
    setattr(settings, "COLTRANE", {"SITE_URL": "http://test-site.com"})
    assert get_site_url() == "http://test-site.com"


def test_get_title(settings):
    setattr(settings, "COLTRANE", {"TITLE": "test-title"})
    assert get_title() == "test-title"


def test_get_description(settings):
    setattr(settings, "COLTRANE", {"DESCRIPTION": "test description"})
    assert get_description() == "test description"


def test_get_markdown_renderer(settings):
    assert get_markdown_renderer() == "markdown2"

    setattr(settings, "COLTRANE", {"MARKDOWN_RENDERER": "mistune"})
    assert get_markdown_renderer() == "mistune"

    setattr(settings, "COLTRANE", {"MARKDOWN_RENDERER": "invalid-markdown-renderer"})

    with pytest.raises(AssertionError):
        get_markdown_renderer()
