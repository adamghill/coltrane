from django.conf import settings

import pytest

from coltrane.config import DEFAULT_COLTRANE_SETTINGS, get_coltrane_settings


def test_get_coltrane_settings_none():
    setattr(settings, "COLTRANE", {})
    assert get_coltrane_settings() == {}


def test_get_coltrane_settings_default():
    del settings.COLTRANE
    assert get_coltrane_settings() == DEFAULT_COLTRANE_SETTINGS


def test_get_coltrane_settings_invalid_type():
    setattr(settings, "COLTRANE", "str")

    with pytest.raises(AssertionError):
        get_coltrane_settings()
