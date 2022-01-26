from pathlib import Path

from django.conf import settings

from coltrane.config.settings import DEFAULT_MARKDOWN_EXTRAS
from coltrane.renderer import (
    _get_markdown_content_as_html,
    _get_markdown_it_content_as_html,
)


def test_get_markdown_content_as_html_with_frontmatter(tmp_path: Path):
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
    context = {"template": "test-template.html"}
    expected = (rendered_html, context)
    actual = _get_markdown_content_as_html("test-1")

    assert actual == expected


def test_get_markdown_content_as_html_extras_settings(tmp_path: Path):
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
    context = {"template": "test-template.html"}
    expected = (rendered_html, context)
    actual = _get_markdown_content_as_html("test-1")

    assert actual == expected

    settings.COLTRANE["MARKDOWN_EXTRAS"] = DEFAULT_MARKDOWN_EXTRAS


test_md = """
---
template: www/content.html
heading1: About
---

[devmarks.io](https://www.devmarks.io) was built because, as a developer, I have a few different sites where I store "things I want to remember later". Code repositories, packages in different programming languages, articles, code samples, and blog posts are scattered across the internet. I wanted to be able to access them all from one place, sort them, filter them, and keep track of when they're updated.

But, it's more than just another bookmarking site. It's smart! Well, not like, "drive you around without touching the steering wheel smart" or anything. And no trendy artificial intelligence (although maybe I'll add some fancy machine learning when I need to raise money to CHANGE THE WORLD with bookmarks!). But, [devmarks.io](https://www.devmarks.io) collects as much metadata as possible from the sites that developers use the most.

If you bookmark a package from one of over 15 supported package repositories, [devmarks.io](https://www.devmarks.io) will collect information about it including the authors, homepage, latest releases, and more. Basically, everything it can find that is available. GitHub repositories show the number of stars and forks, extra data is show for dev.to articles, and many other sites have custom extractors to retrieve as much metadata as possible from whatever you bookmark.

Developer sites automatically sync to [devmarks.io](https://www.devmarks.io) as well. All your disparate data will be consolidated into one central location. I mean, not _every_ site. Not yet. Really... it's just GitHub stars and public Pinboard bookmarks right now. But, many more are coming soon, I promise!

So, yeah. A reasonable amount of smartness.

Hopefully it's as helpful for you as it has been for me!

If you have any comments, questions, concerns, or quibbles please reach out to [me on Twitter](https://twitter.com/adamghill). I'd love to hear from you.

"""


def test_get_markdown_content_as_html_with_frontmatter_benchmark(
    tmp_path: Path, benchmark
):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(test_md)

    rendered_html = "<p>test data</p>\n"
    context = {"template": "test-template.html"}
    expected = (rendered_html, context)

    actual = benchmark(_get_markdown_content_as_html, "test-1")
    # assert actual == expected


def test_get_markdown_it_content_as_html_with_frontmatter_benchmark(
    tmp_path: Path, benchmark
):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-1.md").write_text(test_md)

    rendered_html = "\n<p>test data</p>\n"
    context = {"template": "test-template.html"}
    expected = (rendered_html, context)

    actual = benchmark(_get_markdown_it_content_as_html, "test-1")
    # assert actual[0] == expected[0]
