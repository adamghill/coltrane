from pathlib import Path
from unittest.mock import patch

from coltrane.config.paths import get_base_directory


def test_get_base_directory_no_base_dir_setting(settings):
    delattr(settings, "BASE_DIR")

    with patch("coltrane.config.paths.getcwd", return_value="1234"):
        expected = Path("1234")
        actual = get_base_directory()

        assert actual == expected


def test_get_base_directory_str_base_dir_setting(settings):
    settings.BASE_DIR = "5678"

    expected = Path("5678")
    actual = get_base_directory()

    assert actual == expected
