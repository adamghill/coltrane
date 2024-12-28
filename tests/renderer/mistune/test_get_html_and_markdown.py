from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch

import pytest
from zoneinfo import ZoneInfo

from coltrane.renderer import MistuneMarkdownRenderer
from tests.fixtures import default_site


@pytest.fixture
def markdown_renderer():
    return MistuneMarkdownRenderer()


@patch(
    "coltrane.renderer.MistuneMarkdownRenderer._get_markdown_content_as_html",
    return_value=("some-content", None),
)
def test_handle_none_metadata(_get_markdown_content_as_html, markdown_renderer, default_site):
    markdown_renderer.get_html_and_markdown("some-slug", site=default_site)


def test_publish_date_datetime_in_metadata(markdown_renderer, settings, tmp_path: Path, default_site):
    settings.BASE_DIR = tmp_path
    settings.TIME_ZONE = "UTC"

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
publish_date: 2022-02-26 10:26:02
---
"""
    )

    (_, metadata) = markdown_renderer.get_html_and_markdown("test-1", site=default_site)

    assert isinstance(metadata["publish_date"], datetime)
    assert metadata["publish_date"] == datetime(2022, 2, 26, 10, 26, 2, 0, tzinfo=ZoneInfo(key="UTC"))


def test_publish_date_date_in_metadata(markdown_renderer, settings, tmp_path: Path, default_site):
    settings.BASE_DIR = tmp_path
    settings.TIME_ZONE = "UTC"

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
publish_date: 2022-02-26
---
"""
    )

    (_, metadata) = markdown_renderer.get_html_and_markdown("test-1", site=default_site)

    assert isinstance(metadata["publish_date"], date)
    assert metadata["publish_date"] == datetime(2022, 2, 26, 0, 0, 0, tzinfo=ZoneInfo(key="UTC"))


def test_draft_true_in_metadata(markdown_renderer, settings, tmp_path: Path, default_site):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
draft: true
---
"""
    )

    (_, metadata) = markdown_renderer.get_html_and_markdown("test-1", site=default_site)

    assert isinstance(metadata["draft"], bool)
    assert metadata["draft"]


def test_draft_false_in_metadata(markdown_renderer, settings, tmp_path: Path, default_site):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
draft: false
---
"""
    )

    (_, metadata) = markdown_renderer.get_html_and_markdown("test-1", site=default_site)

    assert isinstance(metadata["draft"], bool)
    assert not metadata["draft"]


def test_draft_string_in_metadata(markdown_renderer, settings, tmp_path: Path, default_site):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
draft: blob
---
"""
    )

    (_, metadata) = markdown_renderer.get_html_and_markdown("test-1", site=default_site)

    assert isinstance(metadata["draft"], bool)
    assert not metadata["draft"]


def test_draft_1_in_metadata(markdown_renderer, settings, tmp_path: Path, default_site):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
draft: 1
---
"""
    )

    (_, metadata) = markdown_renderer.get_html_and_markdown("test-1", site=default_site)

    assert isinstance(metadata["draft"], bool)
    assert not metadata["draft"]
