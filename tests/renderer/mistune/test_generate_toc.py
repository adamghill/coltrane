import pytest

from coltrane.renderer import MistuneMarkdownRenderer


parameters = [
    (
        """
# first header

## second header

### third header

# back to a header

more stuff here
""",
        """
<ul>
  <li>
    <a href="#first-header">first header</a>
    <ul>
      <li>
        <a href="#second-header">second header</a>
        <ul>
          <li><a href="#third-header">third header</a></li>
        </ul>
      </li>
    </ul>
  </li>
  <li>
    <a href="#back-to-a-header">back to a header</a>
  </li>
</ul>
""",
    ),
    (
        """
## second header

## another second header

### third header

# first header

more stuff here
""",
        """
<ul>
  <li>
    <a href="#second-header">second header</a>
  </li>
  <li>
    <a href="#another-second-header">another second header</a>
    <ul>
      <li><a href="#third-header">third header</a></li>
    </ul>
  </li>
  <li>
    <a href="#first-header">first header</a>
  </li>
</ul>
""",
    ),
    ( """
# `code` header

more stuff here
""",
"""
<ul>
  <li>
    <a href="#code-header"><code>code</code> header</a>
  </li>
</ul>
""")
]


@pytest.mark.parametrize("text, expected", parameters)
def test_compare_toc(text, expected):
    markdown_renderer = MistuneMarkdownRenderer()

    (_, metadata) = markdown_renderer.render_markdown_text(text)
    actual = metadata["toc"]

    actual = actual.replace("\n", "").replace("  ", "")
    expected = expected.replace("\n", "").replace("  ", "")
    print(actual)

    assert actual == expected
