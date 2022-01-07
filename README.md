# coltrane

A simple content site framework that harnesses the power of Django without the hassle.

## Features

- Can be a standalone static site or added to `INSTALLED_APPS` to integrate into an existing Django site
- Renders markdown files automatically
- Can use data from JSON files in templates and content
- All the power of Django templates, template tags, and filters
- Can include other Django apps
- Build HTML output for a true static site (coming soon)

Still a little experimental. ;)

## Install

### Create a standalone site

1. Make a new directory for your site and traverse into it: `mkdir new-site && cd new-site`
1. Install `poetry` (if not already installed) to handle Python packages: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
1. Create `poetry` project, add `coltrane` dependency, and install Python packages: `poetry init --no-interaction --dependency coltrane-web:latest && poetry install`
1. Start a new `coltrane` site: `poetry run coltrane create`
1. Start local development server: `poetry run coltrane play`
1. Go to localhost:8000 in web browser

### Add to an existing Django site

Coming soon.

## Render markdown files

`coltrane` takes the URL slug and looks up a corresponding markdown file in the `content` directory.

For example: http://localhost:8000/this-is-a-good-example/ will render the markdown in `content/this-is-a-good-example.md`. The root (i.e. http://localhost:8000/) will look for `content/index.md`.

If a markdown file cannot be found, the response will be a 404.

## Templates

`coltrane` comes with two minimal templates that get used by default: `coltrane/base.html` and `coltrane/content.html`. Overriding those templates work just like in Django.

### Override base template

Create a file named `templates/coltrane/base.html` in your app to override the base template. By default, it needs to include a `content` block.

```html
{% block content %}{% endblock content %}
```

### Override content template

Create a file named `templates/coltrane/content.html` in your app to override the content template. By default, it needs to include a `content` block for the base template and `{{ content }}` to render the markdown.

Note: `content` is already marked safe so the rendered HTML will be output correctly and you do not need to use a `safe` filter for the content template variable.

```html
{% block content %}{{ content }}{% endblock content %}
```

### Custom template

Specify a custom template with a `template` variable in the markdown frontmatter. The specified template context will include variables from the markdown frontmatter, the rendered markdown in `content`, and JSON data in `data`.

#### `index.md`

```markdown
---
title: This is good content
template: sample_app/new-template.html
---

# Heading 1

This will use sample_app/new-template.html to render content.
```

#### `sample_app/new-template.html`

```html
<title>{{ title }}</title>

{{ content }}
```

#### Generated `index.html`

```html
<title>This is good content</title>

<h1 id="heading-1">Heading 1</h1>

<p>This will use sample_app/new-template.html to render content.</p>
```

## Use JSON data

`coltrane` is designed to be used without a database, however, sometimes it's useful to have access to data inside your templates.

### JSON data file

Create a file named `data.json` in your project folder: `touch data.json`. Add whatever data you want to that file and it will be included in the template context.

#### `data.json`

```JSON
{
    {"answer": 42}
}
```

#### `index.md` file

```markdown
# index

The answer to everything is {{ data.answer }}
```

#### Generated `index.html`

```html
<h1>index</h1>

<p>The answer to everything is 42</p>
```

### JSON data directory

Create a directory named `data` in your project folder: `mkdir data`. Create as many JSON files as you want. The name of the file (without the `json` extension) will be used as the key in the context data.

#### `data/author.json`

```JSON
{
    {"name": "Douglas Adams"}
}
```

#### `index.md` file

```markdown
# index

{{ data.author.name }} is the author
```

#### Generated `index.html`

```html
<h1>index.md</h1>

<p>Douglas Adams is the author</p>
```

## Markdown frontmatter

Markdown frontmatter (i.e. YAML before the actual markdown content) is supported. It will be added to the context variable that is used to render the HTML. The default `base.html` template will use `lang` (to specify the HTML language; defaults to "en"), and `title` variables if they are specified in the frontmatter.

### template

Used to specify a custom template that Django will use to render the markdown.

## Build static HTML

`coltrane record` will build the static HTML. Coming soon.

## Settings

Settings specified in a `COLTRANE` dictionary.

```python
# settings.py

COLTRANE = {
    VIEW_CACHE_SECONDS=60*60,
    MARKDOWN_EXTRAS=[
        "metadata",
    ]
}
```

## VIEW_CACHE_SECONDS

Specifies how long the markdown should be cached when Django is dynamically serving the markdown.

## MARKDOWN_EXTRAS

The features that should be enabled when rendering markdown. A list of all available features: https://github.com/trentm/python-markdown2/wiki/Extras. The default extras are:

```python
[
    "fenced-code-blocks",
    "header-ids",
    "metadata",
    "strike",
    "tables",
    "task_list",
]
```

## What's with the name?

`coltrane` is built on top of the Django web framework, which is named after [Django Reinhardt](https://en.wikipedia.org/wiki/Django_Reinhardt). Following in that tradition, I named this static site framework after [John Coltrane](https://en.wikipedia.org/wiki/John_Coltrane), another jazz musician.

## Other Python static site builder alternatives

- [Combine](https://combine.dropseed.dev/): uses Jinja templates under the hood
- [Pelican](https://blog.getpelican.com/)
- [Nikola](https://getnikola.com/)

## Thanks

- https://twitter.com/willmcgugan/status/1477283879841157123 for the initial inspiration
- https://github.com/wsvincent/django-microframework for the `app.py` idea
- https://olifante.blogs.com/covil/2010/04/minimal-django.html
- https://simonwillison.net/2009/May/19/djng/
- https://stackoverflow.com/questions/1297873/how-do-i-write-a-single-file-django-application
- https://github.com/trentm/python-markdown2
