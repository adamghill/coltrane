from coltrane.renderer import render_markdown_text


def test_render_markdown_text():
    markdown_content = """---
title: My test markdown title
---
    
# {{ title }}
"""
    content, metadata = render_markdown_text(markdown_content)
    assert metadata.get("title") == "My test markdown title"
    assert content.strip() == '<h1 id="title">{{ title }}</h1>'
