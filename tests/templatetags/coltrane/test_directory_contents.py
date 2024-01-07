from pathlib import Path
from unittest.mock import ANY

from django.utils.safestring import SafeString

from coltrane.renderer import StaticRequest
from coltrane.templatetags.coltrane_tags import directory_contents


def test_directory_contents(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "toc": ANY,
            "slug": "test",
            "now": ANY,
        }
    ]
    actual = directory_contents(context)

    assert actual == expected


def test_directory_contents_subdirectory_content(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test1").mkdir()
    (tmp_path / "content/test1/test2.md").write_text("test data")

    context = {"request": StaticRequest("/test1")}
    expected = [
        {
            "template": "coltrane/content.html",
            "toc": ANY,
            "slug": "test1/test2",
            "now": ANY,
        }
    ]
    actual = directory_contents(context)

    assert actual == expected


def test_directory_contents_index_not_included(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test").mkdir()
    (tmp_path / "content/test/index.md").write_text("index")

    context = {"request": StaticRequest("/test")}
    expected = []
    actual = directory_contents(context)

    assert actual == expected


def test_directory_contents_explicit_directory(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test").mkdir()
    (tmp_path / "content/test/test.md").write_text("index")

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "toc": ANY,
            "slug": "test/test",
            "now": ANY,
        }
    ]
    actual = directory_contents(context, directory="test")

    assert actual == expected


def test_directory_contents_title(settings, tmp_path: Path):
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
            "toc": ANY,
            "slug": "test",
            "title": "this is a title",
            "now": ANY,
        }
    ]
    actual = directory_contents(context)

    assert actual == expected


def test_directory_contents_safe_string_subdirectory_content(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test1").mkdir()
    (tmp_path / "content/test1/test2.md").write_text("test data")

    context = {"request": StaticRequest("/test1")}
    expected = [
        {
            "template": "coltrane/content.html",
            "toc": ANY,
            "slug": "test1/test2",
            "now": ANY,
        }
    ]
    actual = directory_contents(context, directory=SafeString("test1"))

    assert actual == expected


def test_directory_contents_exclude(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")
    (tmp_path / "content/another-test.md").write_text("another test")

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "toc": ANY,
            "slug": "test",
            "now": ANY,
        }
    ]
    actual = directory_contents(context, exclude="another-test")

    assert actual == expected


def test_directory_contents_exclude_with_slash(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")
    (tmp_path / "content/another-test.md").write_text("another test")

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "toc": ANY,
            "slug": "test",
            "now": ANY,
        }
    ]
    actual = directory_contents(context, exclude="/another-test")

    assert actual == expected


def test_directory_contents_exclude_with_comma_delimited_string(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")
    (tmp_path / "content/another-test.md").write_text("another test")
    (tmp_path / "content/yet-more-test.md").write_text("another test")

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "toc": ANY,
            "slug": "test",
            "now": ANY,
        }
    ]
    actual = directory_contents(context, exclude="/another-test , yet-more-test")

    assert actual == expected


def test_directory_contents_order_by(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")
    (tmp_path / "content/another-test.md").write_text("another test")
    (tmp_path / "content/yet-more-test.md").write_text("another test")

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "toc": None,
            "slug": "another-test",
            "now": ANY,
        },
        {
            "template": "coltrane/content.html",
            "toc": None,
            "slug": "test",
            "now": ANY,
        },
        {
            "template": "coltrane/content.html",
            "toc": None,
            "slug": "yet-more-test",
            "now": ANY,
        },
    ]
    actual = directory_contents(context, order_by="slug")

    assert actual == expected


def test_directory_contents_order_by_reversed(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")
    (tmp_path / "content/another-test.md").write_text("another test")
    (tmp_path / "content/yet-more-test.md").write_text("another test")

    context = {"request": StaticRequest("/")}
    expected = [
        {
            "template": "coltrane/content.html",
            "toc": None,
            "slug": "yet-more-test",
            "now": ANY,
        },
        {
            "template": "coltrane/content.html",
            "toc": None,
            "slug": "test",
            "now": ANY,
        },
        {
            "template": "coltrane/content.html",
            "toc": None,
            "slug": "another-test",
            "now": ANY,
        },
    ]
    actual = directory_contents(context, order_by="-slug")

    assert actual == expected
