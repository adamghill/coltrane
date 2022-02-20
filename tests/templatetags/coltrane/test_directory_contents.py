from pathlib import Path
from unittest.mock import ANY

from django.conf import settings

from coltrane.renderer import StaticRequest
from coltrane.templatetags.coltrane_tags import directory_contents


def test_directory_contents(tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "slug": "test",
            "now": ANY,
        }
    ]
    actual = directory_contents(context)

    assert actual == expected


def test_directory_contents_subdirectory_content(tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test").mkdir()
    (tmp_path / "content/test/test.md").write_text("test data")

    context = {"request": StaticRequest("/test")}
    expected = [
        {
            "template": "coltrane/content.html",
            "slug": "test/test",
            "now": ANY,
        }
    ]
    actual = directory_contents(context)

    assert actual == expected


def test_directory_contents_index_not_included(tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test").mkdir()
    (tmp_path / "content/test/index.md").write_text("index")

    context = {"request": StaticRequest("/test")}
    expected = []
    actual = directory_contents(context)

    assert actual == expected


def test_directory_contents_explicit_directory(tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test").mkdir()
    (tmp_path / "content/test/test.md").write_text("index")

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "slug": "test/test",
            "now": ANY,
        }
    ]
    actual = directory_contents(context, directory="test")

    assert actual == expected


def test_directory_contents_title(tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text(
        """---
title: this is a title
---

index
"""
    )

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "slug": "test",
            "title": "this is a title",
            "now": ANY,
        }
    ]
    actual = directory_contents(context)

    assert actual == expected
