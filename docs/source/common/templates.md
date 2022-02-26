# Templates

`coltrane` comes with two minimal templates that get used by default: `coltrane/base.html` and `coltrane/content.html`. Overriding those templates work just like in Django.

## Override included templates

### `coltrane/base.html`

Create a file named `templates/coltrane/base.html` in your app to override the base template. By default, it needs to include a `content` block.

```html
{% block content %}{% endblock content %}
```

### `coltrane/content.html`

Create a file named `templates/coltrane/content.html` in your app to override the content template. By default, it needs to include a `content` block for the base template and `{{ content }}` to render the markdown.

```{note}
The `content` template variable is already "marked safe" so you do not need to use a `safe` filter.
```

```html
{% block content %}{{ content }}{% endblock content %}
```

## Custom template

Specify a custom template with a `template` variable in the markdown frontmatter.

**`content/index.md`**

```markdown
---
title: This is good content
template: sample_app/new-template.html
---

# Heading 1

This will use sample_app/new-template.html to render content.
```

**`sample_app/new-template.html`**

```html
<title>{{ title }}</title>

{{ content }}
```

**Generated `index.html`**

```html
<title>This is good content</title>

<h1 id="heading-1">Heading 1</h1>

<p>This will use sample_app/new-template.html to render content.</p>
```

## Template context

The specified template context includes:

- all variables from the markdown frontmatter
- rendered markdown HTML in `content`
- JSON data from the `data` directory
- `now` which provides the current `datetime` (would be the time of HTML rendering for static site)
- `request` which provides the current request for an integrated or standalone site
- `debug` which contains the the `DEBUG` setting for an integrated or standalone site (if `INTERNAL_IPS` has the current request's IP which is usually `127.0.0.1` for local development)
- `slug` which contains the current file's "slug" (would be `articles/some-new-article` if there was a markdown file at `content/articles/some-new-article.md`)

**`data/index.json`**

```json
{ "test": "Great" }
```

**`content/index.md`**

```markdown
---
this_is_a_variable: This is a good test
template: some_app/custom-template.html
---

{{ this_is_a_variable }}

Data from JSON files: {{ data.index.test }}

Current datetime: {{ now }}
```

**`some_app/templates/some_app/custom-template.html`**

```html
{{ content }}
```

**Generated `index.html`**

```html
<p>This is a good test</p>

<p>Data from JSON files: Great</p>

<p>Current datetime: 8 Jan. 11, 2022, 10:02 p.m.</p>
```

## Template tags

Template tags are the way for Django templates to use Python code. Django has a [large list of built-in template tags](https://docs.djangoproject.com/en/stable/ref/templates/builtins/) for everything from looping over objects, date formatting, boolean logic with `if`/`else` blocks, or getting the length of an object. By default, all template tags in Django are available in markdown content files.

### Coltrane template tags

#### `directory_contents`

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

{% directory_contents "articles" as directory_contents %}

{% for content in directory_contents %}

- {{ content.slug }}

{% endfor %}
```

```html
<h1 id="articles">Articles</h1>

<ul>
  <li>article1</li>
  <li>article2</li>
</ul>
```

#### `include_md`

Similar to the [`include`](https://docs.djangoproject.com/en/stable/ref/templates/builtins/#include) template tag, but can be used to include a markdown file and have it render correctly into HTML. It can be used in markdown files or in HTML templates.

```markdown
# include_md

{% include_md '_partial.md' %}
```

```html
<h1>include_md</h1>

{% include_md '_partial.md' %}
```

#### `parent`

A `filter` that returns the parent directory for a particular path. Can be passed a `request` or a `string`.

```html
<!-- request of http://localhost/articles/some-article -->
{{ request|parent }} == '/articles'
```

```html
{{ 'http://localhost/articles/some-article'|parent|parent }} == ''
```

### Humanize template tags

`django.contrib.humanize` [includes a useful template tags](https://docs.djangoproject.com/en/stable/ref/contrib/humanize/) to format numbers and dates in human-friendly ways. Normally it needs to be enabled and loaded in templates manually, but `coltrane` enables it by default so it is available to use in markdown content files automatically.

### Custom template tags

`coltrane` will automatically include any custom template tags it finds in the `templatetags` directory to be used in markdown content files.

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
{{ "This"|test }}
```

**Generated `index.html`**

```html
This is a test
```
