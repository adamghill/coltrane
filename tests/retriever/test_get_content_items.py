from pathlib import Path

from coltrane.retriever import get_content_items


def test_location(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")

    actual = get_content_items()

    assert len(actual) == 1
    assert actual[0].relative_url == "/test"
