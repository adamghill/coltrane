from coltrane.views import _normalize_slug


def test_normalize_slug_default():
    expected = "index"
    actual = _normalize_slug("")

    assert actual == expected


def test_normalize_slug_forward_slash():
    expected = "index"
    actual = _normalize_slug("/")

    assert actual == expected


def test_normalize_slug_both_slashes():
    expected = "test-slug"
    actual = _normalize_slug("/test-slug/")

    assert actual == expected


def test_normalize_slug_startswith_slash():
    expected = "test-slug"
    actual = _normalize_slug("/test-slug")

    assert actual == expected


def test_normalize_slug_endswith_slash():
    expected = "test-slug"
    actual = _normalize_slug("test-slug/")

    assert actual == expected


def test_normalize_slug_none():
    expected = "index"
    actual = _normalize_slug(None)

    assert actual == expected
