from os import environ

from coltrane import _get_from_env_or_settings
from tests.fixtures import *  # noqa: F403


def test_get_from_env_or_settings_default():
    expected = "content1"

    settings = {}
    actual = _get_from_env_or_settings(settings, "CONTENT_DIRECTORY", "content1")

    assert expected == actual


def test_get_from_env_or_settings_in_settings():
    expected = "content2"

    settings = {"COLTRANE": {"CONTENT_DIRECTORY": "content2"}}
    actual = _get_from_env_or_settings(settings, "CONTENT_DIRECTORY", "content1")

    assert expected == actual


def test_get_from_env_or_settings_in_environment(env):
    expected = "content3"

    environ["COLTRANE_CONTENT_DIRECTORY"] = "content3"
    settings = {"COLTRANE": {"CONTENT_DIRECTORY": "content2"}}
    actual = _get_from_env_or_settings(settings, "CONTENT_DIRECTORY", "content1")

    assert expected == actual
