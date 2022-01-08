from django.core.cache import caches
from django.core.cache.backends.base import BaseCache

from ..config.settings import get_coltrane_settings


AVAILABLE_CACHE_SETTINGS_KEYS = [
    "VIEW_CACHE",
    "DATA_CACHE",
]


def _get_cache_enabled(settings_key: str) -> bool:
    """
    Get whether a cache is enabled or not for a particular settings key.
    """

    assert settings_key in AVAILABLE_CACHE_SETTINGS_KEYS

    sentinel = object()
    return (
        get_coltrane_settings().get(settings_key, {}).get("SECONDS", sentinel)
        != sentinel
    )


def _get_cache_seconds(settings_key: str) -> bool:
    """
    Get cache seconds for a particular settings key.
    """

    assert _get_cache_enabled(settings_key), f"{settings_key} is not enabled"

    return get_coltrane_settings()[settings_key]["SECONDS"]


def _get_cache_key_namespace(settings_key: str) -> str:
    """
    Get cache key for a particular settings key.
    """

    assert _get_cache_enabled(settings_key), f"{settings_key} is not enabled"

    return f"coltron:{settings_key}:"


def _get_cache_name(settings_key: str) -> str:
    """
    Get cache name for a particular settings key.
    """

    assert _get_cache_enabled(settings_key), f"{settings_key} is not enabled"

    return get_coltrane_settings()[settings_key].get("CACHE_NAME", "default")


def get_view_cache_enabled() -> bool:
    """
    Get whether the view cache is enabled or not.
    """

    return _get_cache_enabled("VIEW_CACHE")


def get_view_cache_seconds() -> int:
    """
    Get how long to cache the view from settings.
    """

    return _get_cache_seconds("VIEW_CACHE")


def get_view_cache_name() -> str:
    """
    Get the view cache name.
    """

    return _get_cache_name("VIEW_CACHE")


def get_view_cache() -> BaseCache:
    """
    Get the view cache.
    """

    return caches[get_view_cache_name()]


def get_view_cache_key(slug: str) -> str:
    """
    Get the view cache key.
    """

    cache_namespace = _get_cache_key_namespace("VIEW_CACHE")

    return f"{cache_namespace}{slug}"


def get_data_cache_enabled() -> bool:
    """
    Get whether the data cache is enabled or not.
    """

    return _get_cache_enabled("DATA_CACHE")


def get_data_cache_seconds() -> int:
    """
    Get how long to cache the view from settings.
    """

    return _get_cache_seconds("DATA_CACHE")


def get_data_cache_key() -> str:
    """
    Get the data cache key.
    """

    cache_namespace = _get_cache_key_namespace("DATA_CACHE")

    return f"{cache_namespace}data"
