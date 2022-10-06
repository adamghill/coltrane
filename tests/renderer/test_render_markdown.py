from dataclasses import dataclass
from pathlib import Path
from typing import Dict
from unittest.mock import patch

from coltrane.renderer import StaticRequest, render_markdown


def test_render_markdown(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-2.md").write_text(
        """---
template: test-template.html
---

test data
"""
    )

    expected_template = "test-template.html"
    expected_content = "<p>test data</p>\n"
    expected_data = {}

    static_request = StaticRequest(path="/")

    rendered_markdown = render_markdown("test-2", static_request)

    assert rendered_markdown.content == expected_template
    assert rendered_markdown.metadata.get("content") == expected_content
    assert rendered_markdown.metadata.get("data") == expected_data
    assert rendered_markdown.metadata.get("template") == expected_template


@dataclass
class MarkdownContent:
    metadata: Dict

    def __str__(self):
        return "test-content"


@patch("coltrane.renderer.markdown_path", return_value=MarkdownContent(metadata=None))
def test_render_markdown_metadata(settings, tmp_path: Path):
    static_request = StaticRequest(path="/")

    rendered_markdown = render_markdown("test-2", static_request)
    assert rendered_markdown.metadata.get("content") == "test-content"
