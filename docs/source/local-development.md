# Local Development

`Markdown` files are rendered into HTML dynamically based on the URL that is requested.

## Create a new site

1. `poetry run coltrane create` to create the folder structure for a new site.

## Generated `coltrane` file structure

```bash
.
├── __init__.py
├── app.py
├── content
│   └── index.md
├── data
├── poetry.lock
└── pyproject.toml
```

## Markdown Content

Add `markdown` files or sub-directories to the `content` directory and rendered HTML will be accessible via auto-generated routes.

- `/` would render the `markdown` in `content/index.md`
- `/about/` would render the `markdown` in `content/about.md`
- `/articles/this-is-the-first-article/` would render the content from `/content/articles/this-is-the-first-article.md`
- `/not-there/` will 404

## HTML Content

If a `markdown` file can not be found for the URL slug, but there is an HTML file with the same slug, it will be served automatically.

- `/app/` would render the HTML in `/templates/app.html` or `/templates/app/index.html`

A filename with an asterisk can be used as a "wildcard" and will be served for any slug that does not have a matching `markdown` or HTML file.

- `/app/some-user` would render the HTML from `/templates/app/*.html`

## Development server

`poetry run coltrane play` will serve the content for local development.

```{warning}
`poetry run coltrane play` is fine for development, but should never be used in production.
```
