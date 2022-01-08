from django.conf import settings

from coltrane.config import DEFAULT_VIEW_CACHE_SECONDS, get_view_cache_seconds


def test_get_view_cache_seconds_default():
    setattr(settings, "COLTRANE", {})
    assert get_view_cache_seconds() == DEFAULT_VIEW_CACHE_SECONDS


def test_get_view_cache_seconds_none():
    setattr(settings, "COLTRANE", {"VIEW_CACHE_SECONDS": None})
    assert get_view_cache_seconds() is None


def test_get_view_cache_seconds_configured():
    setattr(settings, "COLTRANE", {"VIEW_CACHE_SECONDS": 123})
    assert get_view_cache_seconds() == 123
