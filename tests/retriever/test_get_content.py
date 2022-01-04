from unittest.mock import patch

import pytest

from coltrane.retriever import get_content


def test_get_content(tmp_path):
    with patch("coltrane.retriever.getcwd") as getcwd:
        getcwd.return_value = str(tmp_path)

        (tmp_path / "content").mkdir()
        (tmp_path / "content" / "test-1.md").write_text("# test 1")

        contents = get_content()

    assert contents
    assert len(contents) == 1
    assert contents[0].name == "test-1.md"


def test_get_content_with_folder(tmp_path):
    with patch("coltrane.retriever.getcwd") as getcwd:
        getcwd.return_value = str(tmp_path)

        (tmp_path / "content").mkdir()
        (tmp_path / "content" / "test-1.md").write_text("# test 1")

        (tmp_path / "content" / "test-folder").mkdir()
        (tmp_path / "content" / "test-folder" / "test-2.md").write_text("# test 2")

        contents = get_content()

    assert contents
    assert len(contents) == 2
    assert contents[0].name == "test-2.md"
    assert contents[1].name == "test-1.md"


def test_get_content_no_content(tmp_path):
    with patch("coltrane.retriever.getcwd") as getcwd:
        getcwd.return_value = str(tmp_path)

        (tmp_path / "content").mkdir()

        contents = get_content()

    assert len(contents) == 0


def test_get_content_missing_content_directory(tmp_path):
    with patch("coltrane.retriever.getcwd") as getcwd:
        getcwd.return_value = str(tmp_path)

        with pytest.raises(FileNotFoundError):
            get_content()
