from pathlib import Path

from coltrane.config.paths import get_file_path


def test_get_file_path(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test.txt").write_text("test")

    expected = "test"

    actual = get_file_path("test.txt")
    assert actual.exists()

    assert expected == actual.read_text()


def test_get_file_path_not_exists(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()

    actual = get_file_path("test1234.txt")
    assert not actual.exists()
