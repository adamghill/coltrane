from unittest.mock import MagicMock, patch

from coltrane.middleware import IsSecureMiddleware


def test_is_secure_false(rf):
    request = rf.get("/")
    assert request.is_secure() is False

    IsSecureMiddleware(MagicMock())(request)

    assert request.is_secure() is False


@patch("coltrane.config.settings.get_is_secure")
def test_is_secure_true(get_is_secure, rf):
    get_is_secure.return_value = True

    request = rf.get("/")
    assert request.is_secure() is False

    IsSecureMiddleware(MagicMock())(request)

    assert request.is_secure() is True
