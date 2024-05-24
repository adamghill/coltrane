# CLI

## Create

`coltrane create` creates a default project with the all of the files it requires.

### Generated files

```bash
.
├── .gitignore
├── Dockerfile
├── README.md
├── pyproject.toml
└── site
    ├── .env
    ├── .watchmanconfig
    ├── __init__.py
    ├── app.py
    ├── content
    │   └── index.md
    ├── data
    ├── gunicorn.conf.py
    ├── static
    └── templates
```

#### `.gitignore`

Prevent committing certain files.

#### `Dockerfile`

Example `Dockerfile` for deployment.

#### `README.md`

Example readme file.

#### `pyproject.toml`

Lists dependencies as a standard `pyproject.toml` file. Can be used by `pip`, `uv`, `hatch`, `pdm`, and other Python package managers to install dependencies.

#### `site/.env`

Example environment variables.

#### `site/.watchmanconfig`

Prevent `node_modules` directory from triggering excessive restarts of the development server.

#### `site/__init__.py`

Denote the folder is a Python module.

#### `site/app.py`

The entry point for `coltrane` apps. Similar to a standard `manage.py` file in `Django`.

#### `site/content`

Standard directory for `markdown` files.

#### `site/data`

Standard directory for `JSON` files.

#### `site/gunicorn.conf.py`

Example `gunicorn.conf.py` for production deployment.

#### `site/templates`

Standard directory for `HTML` template files.

### Force creation

`coltrane create --force`

Force the creation of a new `coltrane` site even if there is an existing one.

## Play

`coltrane play`

Starts a development webserver to render the markdown files into HTML. Defaults to `127.0.0.1:8000`.

### Port

The port to use rather than the default `8000`.

`coltrane play --port 8001` would start the development server at `127.0.0.1:8001`.

## Record

`coltrane record`

Builds the static site from `markdown` content and stores the HTML in the `output` directory. Stores static files in the `output/static/` directory.

### Incremental builds

By default, `coltrane` will only build markdown files that have changed since the last build. To force re-building all files use `--force`.

`coltrane record --force`

### Output directory

By default `coltrane` will write all files to a directory named `output`. But, that can be overriden with `--output`.

`coltrane record --output public`

### Multithreaded

By default `coltrane` tries to use the optimal number of threads. But, the number of threads to use can be overriden with `--threads`.

`coltrane record --threads 2`

### Ignore errors

By default `coltrane` will exit with a status code of 1 if there is an error while rendering the markdown into HTML. Those errors can be ignore with `--ignore`.

`coltrane record --ignore`
