from django.conf import settings

import pytest

from coltrane.config.cache import get_view_cache_seconds


def test_get_view_cache_seconds_none():
    setattr(settings, "COLTRANE", {"VIEW_CACHE": {"SECONDS": None}})
    assert get_view_cache_seconds() is None


def test_get_view_cache_seconds_configured():
    setattr(settings, "COLTRANE", {"VIEW_CACHE": {"SECONDS": 123}})
    assert get_view_cache_seconds() == 123


def test_get_view_cache_seconds_assert_not_enabled():
    setattr(settings, "COLTRANE", {})

    with pytest.raises(AssertionError):
        get_view_cache_seconds()
