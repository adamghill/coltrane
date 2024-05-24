# Template tags

Template tags are the way for Django templates to use Python code. Django has a [large list of built-in template tags](https://docs.djangoproject.com/en/stable/ref/templates/builtins/) for everything from looping over objects, date formatting, boolean logic with `if`/`else` blocks, or getting the length of an object. By default, all template tags in Django are available in markdown content files.

## Humanize template tags

`django.contrib.humanize` [includes a useful template tags](https://docs.djangoproject.com/en/stable/ref/contrib/humanize/) to format numbers and dates in human-friendly ways. Normally it needs to be enabled and loaded in templates manually, but `coltrane` enables it by default so it is available to use in markdown content files automatically.

## Coltrane template tags

### `directory_contents`

A list of the content at a particular directory.

**List markdown files based on the request path**

If the request url is https://localhost:8000/ and there are these files:

- content/test1.md
- content/test2.md

```markdown
# Contents

{% directory_contents as directory_contents %}

{% for content in directory_contents %}

- {{ content.slug }}

{% endfor %}
```

```html
<h1 id="contents">Contents</h1>

<ul>
  <li>test1</li>
  <li>test2</li>
</ul>
```

**List markdown files based on a particular directory**

If the request url is https://localhost:8000/ and there are these files:

- content/articles/article1.md
- content/articles/article2.md

```markdown
# Articles

{% directory_contents 'articles' as directory_contents %}

{% for content in directory_contents %}

- {{ content.slug }}

{% endfor %}
```

```html
<h1 id='articles'>Articles</h1>

<ul>
  <li>article1</li>
  <li>article2</li>
</ul>
```

**Exclude a slug from being included**

If the request url is https://localhost:8000/ and there are these files:

- content/articles/article1.md
- content/articles/article2.md

```markdown
# Articles

{% directory_contents 'articles' exclude='article1' as directory_contents %}

{% for content in directory_contents %}

- {{ content.slug }}

{% endfor %}
```

```html
<h1 id="articles">Articles</h1>

<ul>
  <li>article2</li>
</ul>
```

**Sort the results of the directory**

The `order_by` kwarg will sort the results by a particular `key`. Available `keys` are `slug`, `now`, and anything in the YAML frontmatter. All keys will be coerced to strings and if a `key` is missing an empty string will be used by default.

If the request url is https://localhost:8000/ and these files are present in the `content` directory:

- content/article1.md
- content/article2.md

```markdown
# Sorted Articles

{% directory_contents order_by='slug' as directory_contents %}

{% for content in directory_contents %}

- {{ content.slug }}

{% endfor %}
```

```html
<h1 id="sorted-articles">Sorted Articles</h1>

<ul>
  <li>article1</li>
  <li>article2</li>
</ul>
```

```markdown
# Reverse Sorted Articles

{% directory_contents order_by='-slug' as directory_contents %}

{% for content in directory_contents %}

- {{ content.slug }}

{% endfor %}
```

```html
<h1 id="reverse-sorted-articles">Reverse Sorted Articles</h1>

<ul>
  <li>article2</li>
  <li>article1</li>
</ul>
```

### `include_md`

Similar to the [`include`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#include) template tag, but can be used to include a markdown file and have it render correctly into HTML. It can be used in markdown files or in HTML templates.

```markdown
# include_md

{% include_md '_partial.md' %}
```

```html
<h1>include_md</h1>

{% include_md '_partial.md' %}
```

### `parent`

A `filter` that returns the parent directory for a particular path. Can be passed a `request` or a `string`.

```html
<!-- request of http://localhost/articles/some-article -->
{{ request|parent }} == '/articles'
```

```html
{{ 'http://localhost/articles/some-article'|parent|parent }} == ''
```

### `to_html`

Convert raw markdown text to html. This is probably the most useful when using `coltrane` as a `Django app`.

`views.py`
```python
def my_view(request):
    markdown_text = """---
title: Article 1
---

# {{ title }}
"""
    ...
```

`my_template.html`
```html
<main>
    {{ markdown_text|to_html }}
</main>
```

Rendered html content
```html
<main>
   <h1>Article 1</h1>
</main>
```

### `raise_404`

Raises a 404 from template. Can be useful when using wildcard HTML templates.

### `last_path`

Gets the last portion the URL path, e.g. the last path of `/app/user/123` would be `"123"`.

### `paths`

Gets all parts of the path as a list of strings, e.g. the paths of `/app/user/123` would be `["app", "user", "123"]`.

## Custom template tags

`coltrane` will automatically enable any template tags it finds in the `templatetags` directory to be used in `markdown` or HTML templates.


**`templatetags/custom_tags.py`**

```python
from django import template

register = template.Library()

@register.filter(name="test")
def test(value, arg):
    return value + " is a test"
```

**`content/index.md`**

```markdown
{{ 'This'|test }}
```

**Generated `index.html`**

```html
This is a test
```

````{note}
For `integrated` mode, custom template tags can be loaded like normal in the markdown file.

**`content/index.md`**

```markdown
{% load custom_tags %}

{{ "This"|some_custom_filter }}
```
````