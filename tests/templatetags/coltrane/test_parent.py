import pytest

from coltrane.templatetags.coltrane_tags import NoParentError, parent


class WSGIRequest:
    @property
    def path(self):
        return "/test2/test2"


def test_parent():
    expected = "/test1"
    actual = parent("/test1/test2")

    assert actual == expected


def test_parent_wsgi_request():
    expected = "/test2"
    actual = parent(WSGIRequest())

    assert actual == expected


def test_parent_ends_with_slash():
    expected = "/test1"
    actual = parent("/test1/test2/")

    assert actual == expected


def test_parent_get_root():
    expected = ""
    actual = parent("/test1")

    assert actual == expected


def test_parent_no_parent_exception():
    with pytest.raises(NoParentError):
        parent("/")


def test_parent_no_parent_exception2():
    with pytest.raises(NoParentError):
        parent("")
