import pytest

from coltrane.renderer import MistuneMarkdownRenderer

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


@pytest.mark.skip("Not needed since there is only one markdown renderer now")
@pytest.mark.parametrize("text", markdown_texts)
def test_compare_code(text):
    mistune_markdown_renderer = MistuneMarkdownRenderer()

    (
        mistune_content,
        _,
    ) = mistune_markdown_renderer.render_markdown_text(text)

    # Remove linebreak differences
    mistune_content = mistune_content.replace("\n", "")

    # assert other_content == mistune_content
