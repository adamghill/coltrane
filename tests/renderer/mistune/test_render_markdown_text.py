import pytest

from coltrane.renderer import MistuneMarkdownRenderer


@pytest.fixture
def markdown_renderer():
    return MistuneMarkdownRenderer()


def test_render_markdown_text(markdown_renderer):
    markdown_content = """---
title: My test markdown title
---

# {{ title }}
"""
    (content, metadata) = markdown_renderer.render_markdown_text(markdown_content)
    expected = '<h1 id="title">{{ title }}</h1>'

    assert metadata.get("title") == "My test markdown title"
    assert content.strip() == expected


def test_render_markdown_text_with_code_fence(markdown_renderer):
    markdown_content = """---
title: My test markdown title
---

# {{ title }}

```
this is a lot of code
```
"""

    (content, metadata) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<h1 id="title">{{ title }}</h1>
{% verbatim %}<pre><code>this is a lot of code
</code></pre>{% endverbatim %}
"""

    assert metadata.get("title") == "My test markdown title"
    assert content == expected


def test_render_markdown_text_with_code_fence_with_language(markdown_renderer):
    markdown_content = """---
title: My test markdown title
---

# {{ title }}

```python
def blob():
    pass
```
"""

    (content, metadata) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<h1 id="title">{{ title }}</h1>
{% verbatim %}<div class="codehilite">
<pre><span></span><code><span class="k">def</span> <span class="nf">blob</span><span class="p">():</span>
    <span class="k">pass</span>
</code></pre>
</div>{% endverbatim %}
"""

    assert metadata.get("title") == "My test markdown title"
    assert content == expected


def test_render_markdown_text_with_code_fence_react(markdown_renderer):
    markdown_content = """---
title: My test markdown title
---

# {{ title }}

```javascript
function App() {
  return (
    <div style={{padding: "16px"}}></div>
  );
}
```
"""

    (content, metadata) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<h1 id="title">{{ title }}</h1>
{% verbatim %}<div class="codehilite">
<pre><span></span><code><span class="kd">function</span><span class="w"> </span><span class="nx">App</span><span class="p">()</span><span class="w"> </span><span class="p">{</span>
<span class="w">  </span><span class="k">return</span><span class="w"> </span><span class="p">(</span>
<span class="w">    </span><span class="o">&lt;</span><span class="nx">div</span><span class="w"> </span><span class="nx">style</span><span class="o">=</span><span class="p">{{</span><span class="nx">padding</span><span class="o">:</span><span class="w"> </span><span class="s2">"16px"</span><span class="p">}}</span><span class="o">&gt;&lt;</span><span class="err">/div&gt;</span>
<span class="w">  </span><span class="p">);</span>
<span class="p">}</span>
</code></pre>
</div>{% endverbatim %}
"""  # noqa: E501

    assert metadata.get("title") == "My test markdown title"
    assert content == expected


def test_render_markdown_text_with_back_ticks(markdown_renderer):
    markdown_content = """---
title: My test markdown title
---

# {{ title }}

`this is code`
"""

    (content, metadata) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<h1 id="title">{{ title }}</h1>
<p><code>this is code</code></p>
"""

    assert metadata.get("title") == "My test markdown title"
    assert content == expected


def test_render_markdown_text_with_abbr(markdown_renderer):
    markdown_content = """
The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium
"""

    (content, _) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<p>The <abbr title="Hyper Text Markup Language">HTML</abbr> specification
is maintained by the <abbr title="World Wide Web Consortium">W3C</abbr>.</p>
"""

    assert content == expected


def test_render_href_with_django_template_language_with_spaces(markdown_renderer):
    markdown_content = """
[{{ link_name }}]({{ link_href }})
"""

    (actual, _) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<p><a href="{{ link_href }}">{{ link_name }}</a></p>
"""

    assert actual == expected


def test_render_href_with_django_template_language_without_spaces(markdown_renderer):
    markdown_content = """
[{{ link_name }}]({{link_href}})
"""

    (actual, _) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<p><a href="{{ link_href }}">{{ link_name }}</a></p>
"""

    assert actual == expected


def test_render_img_with_django_template_language(markdown_renderer):
    markdown_content = """
![{{ image_alt }}]({% static 'images/test.jpg' %})
"""

    (actual, _) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<p><img src="{% static 'images/test.jpg' %}" alt="{{ image_alt }}"/></p>
"""

    assert actual == expected


def test_render_img_with_django_template_language_with_spaces(markdown_renderer):
    markdown_content = """
![{{ image_alt }}]({% static 'images/test.jpg' 'more' %})
"""

    (actual, _) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<p><img src="{% static 'images/test.jpg' 'more' %}" alt="{{ image_alt }}"/></p>
"""

    assert actual == expected


def test_render_img_with_django_template_language_with_spaces_double_quotes(
    markdown_renderer,
):
    markdown_content = """
![{{ image_alt }}]({% static "images/test.jpg" "more" %})
"""

    (actual, _) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<p><img src="{% static 'images/test.jpg' 'more' %}" alt="{{ image_alt }}"/></p>
"""

    assert actual == expected


def test_render_img_with_django_template_language_with_kwarg(markdown_renderer):
    markdown_content = """
![{{ image_alt }}]({% static 'images/test.jpg' more={{ something }} %})
"""

    (actual, _) = markdown_renderer.render_markdown_text(markdown_content)
    expected = """<p><img src="{% static 'images/test.jpg' more={{ something }} %}" alt="{{ image_alt }}"/></p>
"""

    assert actual == expected
