# django-static-site

A simple content site framework that harnesses the power of Django without the hassle.

## Features

- Renders markdown files automatically without dealing with urls.py
- Can use data from JSON files in templates and content
- All the power of Django templates, template tags, and filters
- Can include other Django apps
- Generate HTML output for a true static site (coming soon)

Still a little experimental. ;)

## Create a new site

1. `git clone git@github.com:adamghill/django-static-site.git`
1. `poetry add .`
1. Copy `app.py` from https://raw.githubusercontent.com/adamghill/django-static-site/main/example/app.py
1. `mkdir content`
1. `echo "# Index" >> content/index.md`
1. `echo "DEBUG=True\nSECRET_KEY=" >> .env`
1. Create secret key at https://djecrety.ir/ and update .env file above with it
1. `python app.py runserver`
1. Go to localhost:8000 in web browser

## Create content

`django-static-site` takes the URL slug and looks up a corresponding markdown file in the `content` directory.

For example: http://localhost:8000/this-is-a-good-example/ will render the markdown in `content/this-is-a-good-example.md`. If the file cannot be found, the response will be a 404.

## Use data

`django-static-site` is designed to be used without a database, however, sometimes it's useful to have access to data in the templates.

### data.json

Create a file named `data.json`: `echo {} >> data.json`. Add whatever data you want to that file and it will be included in the template context.

`data.json`

```JSON
{
    {"index": {"answer": 42}}
}
```

```markdown
# index.md

{{ data.index.answer }}
```

## data directory

Create a directory named `data`: `mkdir data`. Create as many JSON files as you want. The name of the file will be used as the key in the context data.

`data/index.json`

```JSON
{
    {"author": "Douglas Adams"}
}
```

```markdown
# index.md

{{ data.index.author }}
```

## Override templates

Overriding templates should work just like Django normally does.

### Base template

Create a file named `templates/static_site/base.html` to override the base template. By default, it needs to include a `content` block.

```html
{% block content %}{% endblock content %}
```

### Content template

Create a file named `templates/static_site/content.html` to override the content template. By default, it needs to include a `content` block and `{{ content|safe }}` to render the markdown.

```html
{% block content %}{{ content|safe }}{% endblock content %}
```

## Todo

- Rename `django-static-site` to something better
- Management command to render all markdown to HTML for actually serving static HTML files
- Cookiecutter to create a site easily
- Publish to PyPI
