import pytest

from coltrane.renderer import Markdown2MarkdownRenderer, MistuneMarkdownRenderer


markdown_texts = [
    """
```python
def blob():
    pass
```
""",
    """
```javascript
function blob() {
    return 0
}
```
""",
    """
```
some code here
```
""",
    """
```unknown_some_here
some code here
```
""",
]


@pytest.mark.parametrize("text", markdown_texts)
def test_compare_code(text):
    markdown2_markdown_renderer = Markdown2MarkdownRenderer()
    mistune_markdown_renderer = MistuneMarkdownRenderer()

    (
        markdown2_content,
        _,
    ) = markdown2_markdown_renderer.render_markdown_text(text)

    (
        mistune_content,
        _,
    ) = mistune_markdown_renderer.render_markdown_text(text)

    # Remove linebreak differences
    markdown2_content = markdown2_content.replace("\n", "")
    mistune_content = mistune_content.replace("\n", "")
    print("markdown2_content", markdown2_content)
    print("mistune_content", mistune_content)
    assert markdown2_content == mistune_content
