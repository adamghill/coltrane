from coltrane.renderer import render_markdown_text


def test_render_markdown_text():
    markdown_content = """---
title: My test markdown title
---
    
# {{ title }}
"""
    (content, metadata) = render_markdown_text(markdown_content)
    expected = '<h1 id="title">{{ title }}</h1>'

    assert metadata.get("title") == "My test markdown title"
    assert content.strip() == expected


def test_render_markdown_text_with_code_fence():
    markdown_content = """---
title: My test markdown title
---

# {{ title }}

```
this is a lot of code
```
"""

    (content, metadata) = render_markdown_text(markdown_content)
    expected = """<h1 id="title">{{ title }}</h1>

{% verbatim %}
<pre><code>this is a lot of code
</code></pre>
{% endverbatim %}
"""

    assert metadata.get("title") == "My test markdown title"
    assert content == expected


def test_render_markdown_text_with_code_fence_with_language():
    markdown_content = """---
title: My test markdown title
---

# {{ title }}

```python
def blob():
    pass
```
"""

    (content, metadata) = render_markdown_text(markdown_content)
    expected = """<h1 id="title">{{ title }}</h1>

{% verbatim %}
<div class="codehilite"><pre><span></span><code><span class="k">def</span> <span class="nf">blob</span><span class="p">():</span>
    <span class="k">pass</span>
</code></pre></div>
{% endverbatim %}
"""

    assert metadata.get("title") == "My test markdown title"
    assert content == expected


def test_render_markdown_text_with_code_fence_react():
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

    (content, metadata) = render_markdown_text(markdown_content)
    expected = """<h1 id="title">{{ title }}</h1>

{% verbatim %}
<div class="codehilite"><pre><span></span><code><span class="kd">function</span><span class="w"> </span><span class="nx">App</span><span class="p">()</span><span class="w"> </span><span class="p">{</span><span class="w"></span>
<span class="w">  </span><span class="k">return</span><span class="w"> </span><span class="p">(</span><span class="w"></span>
<span class="w">    </span><span class="o">&lt;</span><span class="nx">div</span><span class="w"> </span><span class="nx">style</span><span class="o">=</span><span class="p">{{</span><span class="nx">padding</span><span class="o">:</span><span class="w"> </span><span class="s2">&quot;16px&quot;</span><span class="p">}}</span><span class="o">&gt;&lt;</span><span class="err">/div&gt;</span><span class="w"></span>
<span class="w">  </span><span class="p">);</span><span class="w"></span>
<span class="p">}</span><span class="w"></span>
</code></pre></div>
{% endverbatim %}
"""

    assert metadata.get("title") == "My test markdown title"
    assert content == expected


def test_render_markdown_text_with_back_ticks():
    markdown_content = """---
title: My test markdown title
---
    
# {{ title }}

`this is code`
"""

    (content, metadata) = render_markdown_text(markdown_content)
    expected = """<h1 id="title">{{ title }}</h1>

<p><code>this is code</code></p>
"""

    assert metadata.get("title") == "My test markdown title"
    assert content == expected
