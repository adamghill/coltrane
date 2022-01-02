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
1. Install `poetry` (if needed): `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
1. Add `coltrane` dependency: `poetry init --dependency coltrane:0.1.0 && poetry install`
1. Initialize `coltrane`: `poetry run coltrane init`
1. Create secret key at https://djecrety.ir/ and update SECRET_KEY in .env
1. Start local development server: `poetry run coltrane play`
1. Go to localhost:8000 in web browser

### Add to an existing Django site

Coming soon.

## Render markdown files

`coltrane` takes the URL slug and looks up a corresponding markdown file in the `content` directory.

For example: http://localhost:8000/this-is-a-good-example/ will render the markdown in `content/this-is-a-good-example.md`. The root (i.e. http://localhost:8000/) will look for `content/index.md`.

If a markdown file cannot be found, the response will be a 404.

## Use JSON data

`coltrane` is designed to be used without a database, however, sometimes it's useful to have access to data inside your templates.

### data.json

Create a file named `data.json`: `echo {} >> data.json`. Add whatever data you want to that file and it will be included in the template context.

`data.json`

```JSON
{
    {"answer": 42}
}
```

```markdown
# index.md

{{ data.answer }} == 42
```

```html
<h1>index.md</h1>

42 == 42
```

### JSON data directory

Create a directory named `data`: `mkdir data`. Create as many JSON files as you want. The name of the file (without the `json` extension) will be used as the key in the context data.

`data/author.json`

```JSON
{
    {"name": "Douglas Adams"}
}
```

```markdown
# index.md

{{ data.author.name }} == Douglas Adams
```

```html
<h1>index.md</h1>

Douglas Adams == Douglas Adams
```

## Override templates

Overriding templates work just like in Django.

### Override base template

Create a file named `templates/coltrane/base.html` in your app to override the base template. By default, it needs to include a `content` block.

```html
{% block content %}{% endblock content %}
```

### Override content template

Create a file named `templates/coltrane/content.html` in your app to override the content template. By default, it needs to include a `content` block for the base template and `{{ content }}` to render the markdown.

```html
{% block content %}{{ content }}{% endblock content %}
```

## Build static HTML

`coltrane record` will build the static HTML. Not currently implemented.

## Thanks

- https://twitter.com/willmcgugan/status/1477283879841157123 for the initial inspiration
- https://github.com/wsvincent/django-microframework for the `app.py` idea
- https://olifante.blogs.com/covil/2010/04/minimal-django.html
- https://simonwillison.net/2009/May/19/djng/
- https://stackoverflow.com/questions/1297873/how-do-i-write-a-single-file-django-application
- https://github.com/trentm/python-markdown2
