import pytest

from coltrane.templatetags.coltrane_tags import _is_content_slug_in_string


def test_is_content_slug_in_string():
    with pytest.raises(TypeError) as e:
        _is_content_slug_in_string("content-slug", 1)  # type: ignore

    assert e.exconly() == "TypeError: Slugs must be a string"
