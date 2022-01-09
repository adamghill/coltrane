# CLI

## Create

`poetry run coltrane create`

Will setup a default `coltrane` project with the following files:

```
/content/index.md
/data/
/__init__.py
/app.py
/.env
```

## Play

`poetry run coltrane play`

Starts a development webserver to render the markdown files into HTML. Defaults to `127.0.0.1:8000`.

### Port

The port to use rather than the default `8000`.

`poetry run coltrane play --port 8001` would start the development server at `127.0.0.1:8001`.

## Record

`poetry run coltrane record`

Builds the static site and stores the HTML in the `output` directory.

### Incremental builds

By default, `coltrane` will only build markdown files that have changed since the last build.
