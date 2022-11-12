from pathlib import Path
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

    (actual_template, actual_context) = render_markdown("test-2", static_request)

    assert actual_template == expected_template
    assert actual_context.get("content") == expected_content
    assert actual_context.get("data") == expected_data
    assert actual_context.get("template") == expected_template


@patch("coltrane.renderer.render_markdown_path", return_value=("test-content", {}))
def test_render_markdown_metadata(settings, tmp_path: Path):
    static_request = StaticRequest(path="/")

    (_, metadata) = render_markdown("test-2", static_request)
    assert metadata.get("content") == "test-content"
