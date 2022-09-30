from pathlib import Path

from coltrane.feeds import ContentFeed


def test_link():
    actual = ContentFeed().link(None)

    assert actual == "http://localhost"


def test_items(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")
    (tmp_path / "content/another-test.md").write_text("another test")

    actual = ContentFeed().items()

    assert len(actual) == 2


def test_item_link(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")

    items = ContentFeed().items()
    actual = ContentFeed().item_link(items[0])

    assert actual == "http://localhost/test"


def test_item_link_site_with_slash(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.COLTRANE["SITE_URL"] = "http://localhost/"

    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text("test data")

    items = ContentFeed().items()
    actual = ContentFeed().item_link(items[0])

    assert actual == "http://localhost/test"


def test_item_title(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text(
        """---
title: test title
description: a description
---

test data
"""
    )

    items = ContentFeed().items()
    actual = ContentFeed().item_title(items[0])

    assert actual == "test title"


def test_item_description(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text(
        """---
title: test title
description: a description
---

test data
"""
    )

    items = ContentFeed().items()
    actual = ContentFeed().item_description(items[0])

    assert actual == "a description"
