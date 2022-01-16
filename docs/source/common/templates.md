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
- JSON data in `data`
- `now` which provides the current `datetime` (would be the time of HTML rendering for static site)
- `request` which provides the current request for an integrated or dynamic site
- `debug` which contains the the `DEBUG` setting for an integrated or dynamic site (if `INTERNAL_IPS` has the current request's IP which is usually `127.0.0.1` for local development)

**`content/index.md`**

```markdown
---
this_is_a_variable: This is a good test
template: some_app/custom-template.html
---

{{ this_is_a_variable }}

Data from JSON files: {{ data.test }}

Current datetime: {{ now }}
```

**`data.json`**

```json
{ "test": "Great" }
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
