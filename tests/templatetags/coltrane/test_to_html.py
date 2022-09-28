from coltrane.templatetags.coltrane_tags import to_html


def test_to_html(request):
    text = """---
title: My test markdown title
---

# {{ title }}
"""
    html = to_html(context={"request": request}, text=text)
    assert html.strip() == '<h1 id="title">My test markdown title</h1>'
