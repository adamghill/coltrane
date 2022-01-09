# Templates

`coltrane` comes with two minimal templates that get used by default: `coltrane/base.html` and `coltrane/content.html`. Overriding those templates work just like in Django.

## Override base template

Create a file named `templates/coltrane/base.html` in your app to override the base template. By default, it needs to include a `content` block.

```html
{% block content %}{% endblock content %}
```

## Override content template

Create a file named `templates/coltrane/content.html` in your app to override the content template. By default, it needs to include a `content` block for the base template and `{{ content }}` to render the markdown.

Note: `content` is already marked safe so the rendered HTML will be output correctly and you do not need to use a `safe` filter for the content template variable.

```html
{% block content %}{{ content }}{% endblock content %}
```

## Custom template

Specify a custom template with a `template` variable in the markdown frontmatter. The specified template context will include variables from the markdown frontmatter, the rendered markdown in `content`, and JSON data in `data`.

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
