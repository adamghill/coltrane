from pathlib import Path
from unittest.mock import ANY

import pytest

from coltrane.config.coltrane import Site
from coltrane.renderer import MistuneMarkdownRenderer
from tests.fixtures import default_site  # noqa: F401


@pytest.fixture
def markdown_renderer():
    return MistuneMarkdownRenderer()


def test_get_markdown_content_as_html_with_frontmatter(markdown_renderer, settings, tmp_path: Path, default_site: Site):
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
    actual = markdown_renderer._get_markdown_content_as_html("test-1", site=default_site)

    assert actual == expected


def test_get_markdown_content_toc(markdown_renderer, settings, tmp_path: Path, default_site: Site):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(
        """
# title

## test data
"""
    )

    expected_content = """<h1 id="title">title</h1>
<h2 id="test-data">test data</h2>
"""

    expected_toc = '<ul><li><a href="#title">title</a><ul><li><a href="#test-data">test data</a></li></ul></li></ul>'

    expected_metadata = {
        "now": ANY,
        "toc": expected_toc,
    }
    expected = (expected_content, expected_metadata)
    actual = markdown_renderer._get_markdown_content_as_html("test-1", site=default_site)

    assert actual == expected
