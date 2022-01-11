from pathlib import Path

from django.conf import settings

from coltrane.renderer import render_markdown


def test_render_markdown(tmp_path: Path):
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

    (actual_template, actual_context) = render_markdown("test-2")

    assert actual_template == expected_template
    assert actual_context.get("content") == expected_content
    assert actual_context.get("data") == expected_data
    assert actual_context.get("template") == expected_template
