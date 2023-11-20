import pytest

from coltrane.templatetags.coltrane_tags import raise_404


def test_raise_404():
    expected = "django.http.response.Http404"

    with pytest.raises(Exception) as e:
        raise_404()

    actual = e.exconly()

    assert expected in actual


def test_raise_404_with_message():
    expected = "django.http.response.Http404: this is a test"

    with pytest.raises(Exception) as e:
        raise_404("this is a test")

    actual = e.exconly()

    assert expected in actual
