from pathlib import Path

from coltrane.sitemaps import ContentSitemap


def test_items(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")
    (tmp_path / "content/another-test.md").write_text("another test")

    actual = ContentSitemap().items()

    assert len(actual) == 2


def test_location(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")

    items = ContentSitemap().items()
    actual = ContentSitemap().location(items[0])

    assert actual == "/test"


def test_location_index(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/index.md").write_text("index")

    items = ContentSitemap().items()
    actual = ContentSitemap().location(items[0])

    assert actual == ""
