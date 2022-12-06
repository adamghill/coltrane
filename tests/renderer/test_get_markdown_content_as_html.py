from pathlib import Path
from unittest.mock import ANY

from coltrane.config.settings import DEFAULT_MARKDOWN_EXTRAS
from coltrane.renderer import _get_markdown_content_as_html


def test_get_markdown_content_as_html_with_frontmatter(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
---

test data
"""
    )

    rendered_html = "<p>test data</p>\n"
    context = {"template": "test-template.html", "toc": ANY, "now": ANY}
    expected = (rendered_html, context)
    actual = _get_markdown_content_as_html("test-1")

    assert actual == expected


def test_get_markdown_content_as_html_extras_settings(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    setattr(settings, "COLTRANE", {})
    settings.COLTRANE["MARKDOWN_EXTRAS"] = [
        "metadata",
    ]

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """---
template: test-template.html
---

test data
"""
    )

    rendered_html = "<p>test data</p>\n"
    context = {"template": "test-template.html", "toc": None, "now": ANY}
    expected = (rendered_html, context)
    actual = _get_markdown_content_as_html("test-1")

    assert actual == expected

    settings.COLTRANE["MARKDOWN_EXTRAS"] = DEFAULT_MARKDOWN_EXTRAS


def test_get_markdown_content_toc(settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """
# title

## test data
"""
    )

    expected_toc = """<ul>
  <li><a href="#title">title</a>
  <ul>
    <li><a href="#test-data">test data</a></li>
  </ul></li>
</ul>
"""

    context = {
        "now": ANY,
        "toc": expected_toc,
    }
    expected = (ANY, context)
    actual = _get_markdown_content_as_html("test-1")

    assert actual == expected
