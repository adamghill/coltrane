import pytest

from coltrane.renderer import StaticRequest


def test_static_request_scheme(settings):
    settings.COLTRANE = {"SITE_URL": "http://localhost"}
    request = StaticRequest(path="/")

    assert request.scheme == "http"


def test_static_request_get_host(settings):
    settings.COLTRANE = {"SITE_URL": "http://localhost"}
    request = StaticRequest(path="/")

    assert request.get_host() == "localhost"


def test_static_request_missing_site(settings):
    settings.COLTRANE = {}
    request = StaticRequest(path="/")

    with pytest.raises(AssertionError):
        request.scheme  # noqa: B018


def test_static_request_missing_coltrane(settings):
    delattr(settings, "COLTRANE")
    request = StaticRequest(path="/")

    with pytest.raises(AssertionError):
        request.scheme  # noqa: B018
