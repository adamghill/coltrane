# CLI

## Create

`poetry run coltrane create` sets up a default `coltrane` project.

### Generated files

```bash
.
├── .env
├── .gitignore
├── .watchmanconfig
├── __init__.py
├── app.py
├── content
│   └── index.md
├── data
├── Dockerfile
├── gunicorn.conf.py
├── templates
├── poetry.lock
└── pyproject.toml
```

#### `.env`

Example environment variables.

#### `.gitignore`

Prevent committing certain files.

#### `.watchmanconfig`

Prevent `node_modules` directory from triggering excessive restarts of the development server.

#### `__init__.py`

Denote the folder is a Python module.

#### `app.py`

The entry point for `coltrane` apps. Similar to a standard `manage.py` file in `Django`.

#### `content`

Standard directory for `markdown` files.

#### `data`

Standard directory for `JSON` files.

#### `Dockerfile`

Example `Dockerfile` for deployment.

#### `gunicorn.conf.py`

Example `gunicorn.conf.py` for deployment.

#### `templates`

Standard directory for `HTML` template files.

#### `poetry.lock`

Lock file for dependencies.

#### `pyproject.toml`

Lists dependencies. More details in the [Poetry documentation](https://python-poetry.org/docs/pyproject/).

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

Builds the static site from `markdown` content and stores the HTML in the `output` directory. Stores static files in the `output/static/` directory.

### Incremental builds

By default, `coltrane` will only build markdown files that have changed since the last build. To force re-building all files use `--force`.

`poetry run coltrane record --force`

### Output directory

By default `coltrane` will write all files to a directory named `output`. But, that can be overriden with `--output`.

`poetry run coltrane record --output public`

### Multithreaded

By default `coltrane` tries to use the optimal number of threads. But, the number of threads to use can be overriden with `--threads`.

`poetry run coltrane record --threads 2`

### Ignore errors

By default `coltrane` will exit with a status code of 1 if there is an error while rendering the markdown into HTML. Those errors can be ignore with `--ignore`.

`poetry run coltrane record --ignore`
