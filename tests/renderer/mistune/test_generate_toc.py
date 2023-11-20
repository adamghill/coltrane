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
    # Not sure how this should function
    #     (
    #         """
    # ## second header
    # ## another second header
    # ### third header
    # # first header
    # more stuff here
    # """,
    #         """
    # <ul>
    #   <li>
    #     <a href="#second-header">second header</a>
    #   </li>
    #   <li>
    #     <a href="#another-second-header">another second header</a>
    #     <ul>
    #       <li><a href="#third-header">third header</a></li>
    #     </ul>
    #   </li>
    #   <li>
    #     <a href="#first-header">first header</a>
    #   </li>
    # </ul>
    # """,
    #     ),
    (
        """
# `code` header

more stuff here
""",
        """
<ul>
  <li>
    <a href="#code-header"><code>code</code> header</a>
  </li>
</ul>
""",
    ),
    (
        """
## second header

## another second header

### third header

#### fourth header

#### another fourth header

### more third header

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
      <li>
        <a href="#third-header">third header</a>
        <ul>
          <li><a href="#fourth-header">fourth header</a></li>
          <li><a href="#another-fourth-header">another fourth header</a></li>
        </ul>
      </li>
      <li>
        <a href="#more-third-header">more third header</a>
      </li>
    </ul>
  </li>
</ul>
""",
    ),
    (
        """
# first

## second

### third

## more second

""",
        """
<ul>
  <li>
    <a href="#first">first</a>
    <ul>
      <li>
        <a href="#second">second</a>
        <ul>
          <li>
            <a href="#third">third</a>
          </li>
        </ul>
      </li>
      <li>
        <a href="#more-second">more second</a>
      </li>
    </ul>
  </li>
</ul>
""",
    ),
    (
        """
# first
""",
        """
<ul>
  <li>
    <a href="#first">first</a>
  </li>
</ul>
""",
    ),
    (
        """
## second
""",
        """
<ul>
  <li>
    <a href="#second">second</a>
  </li>
</ul>
""",
    ),
    (
        """
# first

## second
""",
        """
<ul>
  <li>
    <a href="#first">first</a>
    <ul>
      <li>
        <a href="#second">second</a>
      </li>
    </ul>
  </li>
</ul>
""",
    ),
    (
        """
# first

## second

# another first
""",
        """
<ul>
  <li>
    <a href="#first">first</a>
    <ul>
      <li>
        <a href="#second">second</a>
      </li>
    </ul>
  </li>
  <li>
    <a href="#another-first">another first</a>
  </li>
</ul>
""",
    ),
    (
        """
## first

### second

## another first
""",
        """
<ul>
  <li>
    <a href="#first">first</a>
    <ul>
      <li>
        <a href="#second">second</a>
      </li>
    </ul>
  </li>
  <li>
    <a href="#another-first">another first</a>
  </li>
</ul>
""",
    ),
    (
        """
# first

## second

### third

## another second
""",
        """
<ul>
  <li>
    <a href="#first">first</a>
    <ul>
      <li>
        <a href="#second">second</a>
        <ul>
          <li>
            <a href="#third">third</a>
          </li>
        </ul>
      </li>
      <li>
        <a href="#another-second">another second</a>
      </li>
    </ul>
  </li>
</ul>
""",
    ),
]


def eq(actual, expected):
    # actual = HTML(actual).prettify()
    # expected = HTML(expected).prettify()

    expected = expected.replace("\n", "").replace("  ", "")

    print("actual:")  # noqa: T201
    print(actual)  # noqa: T201
    print("expected:")  # noqa: T201
    print(expected)  # noqa: T201

    assert actual == expected


@pytest.mark.parametrize("text, expected", parameters)
def test_compare_toc(text, expected):
    markdown_renderer = MistuneMarkdownRenderer()

    (_, metadata) = markdown_renderer.render_markdown_text(text)
    actual = metadata["toc"]

    eq(actual, expected)
