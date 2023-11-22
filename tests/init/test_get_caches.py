from os import environ

import pytest

from coltrane import DEFAULT_CACHES_SETTINGS, _get_caches
from tests.fixtures import *  # noqa: F403


@pytest.fixture
def caches_settings():
    return {"CACHES": {"default": {"test": "ok"}}}


def test_get_caches_default():
    expected = DEFAULT_CACHES_SETTINGS
    actual = _get_caches({})

    assert expected == actual


def test_get_caches_override_no_default():
    expected = DEFAULT_CACHES_SETTINGS
    actual = _get_caches({"CACHES": {"test": "no-default"}})

    assert expected == actual


def test_get_caches_override_default(caches_settings):
    expected = {"default": {"test": "ok"}}
    actual = _get_caches(caches_settings)

    assert expected == actual


def test_get_caches_env_dummy(env, caches_settings):
    environ["CACHE"] = "dummy"

    expected = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
    actual = _get_caches(caches_settings)

    assert expected == actual


def test_get_caches_env_invalid(env, caches_settings):
    environ["CACHE"] = "invalid-cache-name"

    with pytest.raises(Exception) as e:
        _get_caches(caches_settings)

    assert e.exconly() == "Exception: Unknown cache backend: 'invalid-cache-name'"


class TestMemory:
    def test_get_caches(self, env, caches_settings):
        environ["CACHE"] = "memory"

        expected = {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "unique-snowflake",
            }
        }
        actual = _get_caches(caches_settings)

        assert expected == actual

    def test_get_caches_location(self, env, caches_settings):
        environ["CACHE"] = "memory"
        environ["CACHE_LOCATION"] = "frosty-snowflake"

        expected = {
            "default": {
                "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
                "LOCATION": "frosty-snowflake",
            }
        }
        actual = _get_caches(caches_settings)

        assert expected == actual


class TestFilesystem:
    def test_get_caches(self, env, caches_settings):
        environ["CACHE"] = "filesystem"
        environ["CACHE_LOCATION"] = "/root/tmp/var"

        expected = {
            "default": {
                "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
                "LOCATION": "/root/tmp/var",
            }
        }
        actual = _get_caches(caches_settings)

        assert expected == actual

    def test_get_caches_missing_location(self, env, caches_settings):
        environ["CACHE"] = "filesystem"

        with pytest.raises(Exception) as e:
            _get_caches(caches_settings)

        assert e.exconly() == "Exception: Missing CACHE_LOCATION: 'filesystem'"


class TestMemcache:
    def test_get_caches(self, env, caches_settings):
        environ["CACHE"] = "memcache"
        environ["CACHE_LOCATION"] = "127.0.0.1"

        expected = {
            "default": {
                "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
                "LOCATION": ["127.0.0.1"],
            }
        }
        actual = _get_caches(caches_settings)

        assert expected == actual

    def test_get_caches_missing_location(self, env, caches_settings):
        environ["CACHE"] = "memcache"

        with pytest.raises(Exception) as e:
            _get_caches(caches_settings)

        assert e.exconly() == "Exception: Missing CACHE_LOCATION: 'memcache'"


class TestRedis:
    def test_get_caches(self, env, caches_settings):
        environ["CACHE"] = "redis"
        environ["CACHE_LOCATION"] = "127.0.0.1"

        expected = {
            "default": {
                "BACKEND": "django.core.cache.backends.redis.RedisCache",
                "LOCATION": ["127.0.0.1"],
            }
        }
        actual = _get_caches(caches_settings)

        assert expected == actual

    def test_get_caches_missing_location(self, env, caches_settings):
        environ["CACHE"] = "redis"

        with pytest.raises(Exception) as e:
            _get_caches(caches_settings)

        assert e.exconly() == "Exception: Missing CACHE_LOCATION: 'redis'"
