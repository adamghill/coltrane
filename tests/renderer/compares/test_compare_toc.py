import pytest

from coltrane.renderer import Markdown2MarkdownRenderer, MistuneMarkdownRenderer


markdown_texts = [
    """
# first header

## second header

### third header

# back to a header

more stuff here
""",
    """
# first header

## second header

### third header

## back to a second header

more stuff here
""",
    """
# first header

## second header

### third header

### another third header

more stuff here
""",
    """
# first header

## second header

### third header

#### fourth header

more stuff here
""",
]


@pytest.mark.parametrize("text", markdown_texts)
def test_compare_toc(text):
    markdown2_markdown_renderer = Markdown2MarkdownRenderer()
    mistune_markdown_renderer = MistuneMarkdownRenderer()

    (
        markdown2_content,
        markdown2_metadata,
    ) = markdown2_markdown_renderer.render_markdown_text(text)

    (
        mistune_content,
        mistune_metadata,
    ) = mistune_markdown_renderer.render_markdown_text(text)

    # Remove slight linebreak differences
    markdown2_content = markdown2_content.replace("\n", "")
    mistune_content = mistune_content.replace("\n", "")
    print("markdown2_content", markdown2_content)
    print("mistune_content", mistune_content)
    assert markdown2_content == mistune_content

    print("markdown2_metadata", markdown2_metadata["toc"])
    print("mistune_metadata", mistune_metadata["toc"])
    assert markdown2_metadata["toc"] == mistune_metadata["toc"]
