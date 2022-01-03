from django.conf import settings

from coltrane.views import DEFAULT_VIEW_CACHE_SECONDS, _get_view_cache_seconds


def test_get_view_cache_seconds_default():
    setattr(settings, "COLTRANE", {})
    assert _get_view_cache_seconds() == DEFAULT_VIEW_CACHE_SECONDS
    del settings.COLTRANE


def test_get_view_cache_seconds_none():
    setattr(settings, "COLTRANE", None)
    assert _get_view_cache_seconds() == DEFAULT_VIEW_CACHE_SECONDS
    del settings.COLTRANE


def test_get_view_cache_seconds_configured():
    setattr(settings, "COLTRANE", {"VIEW_CACHE_SECONDS": 123})
    assert _get_view_cache_seconds() == 123
    del settings.COLTRANE
