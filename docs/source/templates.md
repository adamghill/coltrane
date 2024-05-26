# Templates

`coltrane` comes with two minimal templates that get used by default: `coltrane/base.html` and `coltrane/content.html`. Overriding those templates works just like in Django.

## Override included templates

### `coltrane/base.html`

Create a file named `templates/coltrane/base.html` in your app to override the base template. By default, it needs to include a `content` block.

```html
{% block content %}{% endblock content %}
```

### `coltrane/content.html`

Create a file named `templates/coltrane/content.html` in your app to override the content template. By default, it needs to include a `content` block for the base template and `{{ content }}` to render the markdown.

```{note}
The `content` template variable is already marked "safe" so you do not need to use the `safe` filter.
```

```html
{% block content %}{{ content }}{% endblock content %}
```

## Custom template

Specify a custom template with a `template` variable in the `markdown` frontmatter.

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

**Generated HTML**

```html
<title>This is good content</title>

<h1 id="heading-1">Heading 1</h1>

<p>This will use sample_app/new-template.html to render content.</p>
```

## Error views

Similar to Django's default [error views](https://docs.djangoproject.com/en/stable/ref/views/#error-views) `coltrane` will serve a template if it can find it for certain status codes.

Create any of these HTML files under the `templates` directory and they will be used automatically when `DEBUG=False`.

- 404.html (page not found)
- 500.html (server error)
- 403.html (permission denied)
- 400.html (bad request)
