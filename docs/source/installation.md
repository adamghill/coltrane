# Installation

```{note}
`uv` and `pip` examples are shown below, although most standard Python package managers can be used to install `coltrane`.
```

```{tab} uv
1. [Install `pipx`](https://pipx.pypa.io/stable/installation/)
1. `pipx install uv` to install `uv` globally
1. `mkdir new-site && cd new-site` to create a new folder
1. `uv venv` to create a Python virtual environment in `.venv`
1. `uv pip install "coltrane<1"` to install `coltrane` into the Python virtual environment
```

```{tab} pip
1. `mkdir new-site && cd new-site` to create a new folder
1. `python3 -m venv .venv` to create a Python virtual environment in `.venv`
1. `source .venv/bin/activate` to activate the Python virtual environment
1. `pip install "coltrane<1"` to install `coltrane` into the Python virtual environment
```

```{note}
`brew install watchman` on MacOS for a less resource-intensive local development server.
```

## Extras

`coltrane` has some additional functionality that can also be enabled if extra packages are installed.

```{tab} uv
1. Add any extras between square brackets in the `coltrane` dependency in `pyproject.toml`, e.g. `coltrane[deploy]<1`
1. `uv pip install -r pyproject.toml`
```

```{tab} pip
1. Create a `requirements.txt` file if necessary
1. Add `coltrane<1` to `requirements.txt`
1. Add any extras between square brackets, e.g. `coltrane[deploy]<1`
1. `source .venv/bin/activate` if the virtual environment is not already activated
1. `pip install -r requirements.txt`
```

###  json5

Adds support for using [JSON5](https://json5.org) for [data](data.md) files. This allows trailing commas and comments in JSON, so it can be useful for making JSON a little more readable.

```
coltrane[json5]
```

### `django-compressor`

Adds support for using [`django-compressor`](https://django-compressor.readthedocs.io/) in templates.

```
coltrane[compressor]
```

Use the `compress` templatetag like normal (no need to `load` it in the template).

```html
<head>
    {% compress css %}
    <link href="{% static 'css/styles.css' %}" rel="stylesheet" type="text/css">
    {% endcompress %}
</head>
```

Requires running `python app.py compress` when deployed.

### `deploy`

Adds support for deploying `coltrane` to a production server with `gunicorn` and `whitenoise` pre-configured. More details at [deployment.md](deployment).

```
coltrane[deploy]
```