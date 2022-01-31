from django.conf import settings

import pytest

from coltrane.retriever import get_content


def test_get_content(tmp_path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text("# test 1")

    contents = list(get_content())

    assert contents
    assert len(contents) == 1
    assert contents[0].name == "test-1.md"


def test_get_content_not_markdown(tmp_path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text("# test 1")
    (tmp_path / "content" / "test-2.test").write_text("# test 2")

    contents = list(get_content())

    assert contents
    assert len(contents) == 1
    assert contents[0].name == "test-1.md"


def test_get_content_with_folder(tmp_path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text("# test 1")

    (tmp_path / "content" / "test-folder").mkdir()
    (tmp_path / "content" / "test-folder" / "test-2.md").write_text("# test 2")

    contents = list(get_content())

    assert contents
    assert len(contents) == 2

    contents.sort(key=lambda c: c.name)
    assert contents[0].name == "test-1.md"
    assert contents[1].name == "test-2.md"


def test_get_content_no_content(tmp_path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()

    contents = list(get_content())

    assert len(contents) == 0


def test_get_content_missing_content_directory(tmp_path):
    settings.BASE_DIR = tmp_path

    with pytest.raises(FileNotFoundError):
        list(get_content())
