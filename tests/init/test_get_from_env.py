from unittest.mock import patch

from coltrane import _get_from_env


@patch("coltrane.getenv", return_value="a,b,c")
def test_get_from_env(getenv):  # noqa: ARG001
    expected = ["a", "b", "c"]
    actual = _get_from_env("TEST_SETTING")

    assert actual == expected
