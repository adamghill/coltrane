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

    template = "test-template.html"
    context = {
        "content": "<p>test data</p>\n",
        "data": {},
        "template": "test-template.html",
    }
    expected = (template, context)

    actual = render_markdown("test-2")

    assert actual == expected
