from datetime import datetime
from pathlib import Path

from zoneinfo import ZoneInfo

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


def test_item_pubdate(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text(
        """---
title: test title
description: a description
publish_date: 2024-02-25 22:36:00
---

test data
"""
    )

    settings.TIME_ZONE = "UTC"

    items = ContentFeed().items()
    actual = ContentFeed().item_pubdate(items[0])

    assert actual == datetime(2024, 2, 25, 22, 36, tzinfo=ZoneInfo(key="UTC"))


def test_item_pubdate_with_time_zone(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()
    (tmp_path / "content/test.md").write_text(
        """---
title: test title
description: a description
publish_date: 2024-02-25 22:36:00
---

test data
"""
    )

    settings.TIME_ZONE = "America/Chicago"

    items = ContentFeed().items()
    actual = ContentFeed().item_pubdate(items[0])

    assert actual == datetime(2024, 2, 25, 22, 36, tzinfo=ZoneInfo(key="America/Chicago"))
