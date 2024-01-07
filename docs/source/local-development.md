# Local Development

`markdown` files are rendered into HTML dynamically based on the URL that is requested.

## Create a new site

`poetry run coltrane create` creates the folder structure for a new site.

```{note}
More details about the `create` options and the files that are generated are in [CLI](cli.md#generated-files).
```

## Development server

`poetry run coltrane play` serves the content for local development.

```{warning}
`poetry run coltrane play` is fine for development, but should never be used in production.
```
