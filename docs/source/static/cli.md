# CLI

## Create

`poetry run coltrane create`

Will setup a default `coltrane` project with the following files in the current directory:

```
content/index.md
data/
.env
.watchmanconfig
__init__.py
app.py
```

### Force creation

`poetry run coltrane create --force`

Force the creation of a new `coltrane` site even if there is an existing one.

## Play

`poetry run coltrane play`

Starts a development webserver to render the markdown files into HTML. Defaults to `127.0.0.1:8000`.

### Port

The port to use rather than the default `8000`.

`poetry run coltrane play --port 8001` would start the development server at `127.0.0.1:8001`.

## Record

`poetry run coltrane record`

Builds the static site from markdown content and stores the HTML in the `output` directory. Stores static files in the `output/static/` directory.

### Incremental builds

By default, `coltrane` will only build markdown files that have changed since the last build. To force re-building all files use `--force`.

`poetry run coltrane record --force`

### Multithreaded

By default `coltrane` tries to use the optimal number of threads. But, the number of threads to use can be overriden with `--threads`.

`poetry run coltrane record --threads 2`
