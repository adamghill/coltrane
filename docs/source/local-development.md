# Local Development

`markdown` files are rendered into HTML dynamically based on the URL that is requested.

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

## Development server

`poetry run coltrane play` will serve the content for local development.

```{warning}
`poetry run coltrane play` is fine for development, but should never be used in production.
```
