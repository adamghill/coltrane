# Installation

1. `mkdir new-site && cd new-site` to create a new folder
1. `poetry init --no-interaction --dependency 'coltrane:<1' && poetry install` to create a new virtual environment and install the `coltrane` package
1. Optional: `brew install watchman` on MacOS for less resource-intensive local development server

## Extras

`coltrane` has some additional functionality that is not enabled by default. To add an extra to an existing `Poetry` project use square brackets, e.g. `poetry add coltrane[json5]`. To install multiple extras separate them with commas, e.g. `poetry add coltrane[deploy,json5]`

### `json5`

Adds support for using [JSON5](https://json5.org) for [data](data.md) files. This allows trailing commas and comments in JSON, so it can be useful for making JSON a little more readable.

### `deploy`

Adds support for deploying `coltrane` to a production server with `gunicorn` and `whitenoise` pre-configured. More details at [deployment.md](deployment).
