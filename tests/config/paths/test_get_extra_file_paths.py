from pathlib import Path

from coltrane.config.paths import get_extra_file_paths


def test_get_extra_file_paths(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.COLTRANE["EXTRA_FILE_NAMES"] = ["test.txt"]

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test.txt").write_text("test")

    actual = list(get_extra_file_paths())
    assert len(actual) == 1


def test_get_extra_file_paths_file_does_not_exist(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.COLTRANE["EXTRA_FILE_NAMES"] = ["test.txt"]

    actual = list(get_extra_file_paths())
    assert len(actual) == 0


def test_get_extra_file_paths_setting_is_empty(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.COLTRANE["EXTRA_FILE_NAMES"] = []

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test.txt").write_text("test")

    actual = list(get_extra_file_paths())
    assert len(actual) == 0
