import pytest

from coltrane.config.cache import ViewCache


def test_get_view_cache_seconds_none(settings):
    settings.COLTRANE = {"VIEW_CACHE": {"SECONDS": None}}
    view_cache = ViewCache()
    assert view_cache.seconds is None


def test_get_view_cache_seconds_configured(settings):
    settings.COLTRANE = {"VIEW_CACHE": {"SECONDS": 123}}
    view_cache = ViewCache()
    assert view_cache.seconds == 123


def test_get_view_cache_seconds_assert_not_enabled(settings):
    settings.COLTRANE = {}
    view_cache = ViewCache()

    with pytest.raises(AttributeError):
        view_cache.seconds  # noqa: B018
