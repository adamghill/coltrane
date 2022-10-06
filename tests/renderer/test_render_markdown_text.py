from coltrane.renderer import render_markdown_text


def test_render_markdown_text():
    markdown_content = """---
title: My test markdown title
---
    
# {{ title }}
"""
    rendered_markdown = render_markdown_text(markdown_content)
    assert rendered_markdown.metadata.get("title") == "My test markdown title"
    assert rendered_markdown.content.strip() == '<h1 id="title">{{ title }}</h1>'
