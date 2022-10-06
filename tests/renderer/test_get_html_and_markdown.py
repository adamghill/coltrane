from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from coltrane.renderer import RenderedMarkdown, get_html_and_markdown


@patch(
    "coltrane.renderer._get_markdown_content_as_html",
    return_value=(RenderedMarkdown("some-content", None)),
)
def test_handle_none_metadata(_get_markdown_content_as_html):
    get_html_and_markdown("some-slug")


def test_publish_date_in_metadata(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
publish_date: 2022-02-26 10:26:02
---
"""
    )

    rendered_markdown = get_html_and_markdown("test-1")

    assert isinstance(rendered_markdown.metadata["publish_date"], datetime)
    assert rendered_markdown.metadata["publish_date"] == datetime(2022, 2, 26, 10, 26, 2, 0)


def test_draft_true_in_metadata(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
draft: true
---
"""
    )

    rendered_markdown = get_html_and_markdown("test-1")

    assert isinstance(rendered_markdown.metadata["draft"], bool)
    assert rendered_markdown.metadata["draft"]


def test_draft_false_in_metadata(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
draft: false
---
"""
    )

    rendered_markdown = get_html_and_markdown("test-1")

    assert isinstance(rendered_markdown.metadata["draft"], bool)
    assert not rendered_markdown.metadata["draft"]


def test_draft_string_in_metadata(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
draft: blob
---
"""
    )

    rendered_markdown = get_html_and_markdown("test-1")

    assert isinstance(rendered_markdown.metadata["draft"], bool)
    assert not rendered_markdown.metadata["draft"]


def test_draft_1_in_metadata(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
draft: 1
---
"""
    )

    rendered_markdown = get_html_and_markdown("test-1")

    assert isinstance(rendered_markdown.metadata["draft"], bool)
    assert not rendered_markdown.metadata["draft"]
