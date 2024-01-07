# Installation

1. `mkdir new-site && cd new-site` to create a new folder
1. `poetry init --no-interaction --dependency 'coltrane:<1' && poetry install` to create a new virtual environment and install the `coltrane` package
1. Optional: `brew install watchman` on MacOS for less resource-intensive local development server

## Extra dependencies

`Coltrane` has some additional functionality that is not enabled by default, but can be used if it is installed with extras.

### JSON5 support

Adds support for using [JSON5](https://json5.org) for [data](data.md) files. This allows trailing commas and comments in JSON, so it can be useful for making JSON a little more readable.

`poetry add coltrane -E json5`

### Deployment

Adds support for deploying `Coltrane` to a production server with `gunicorn` and `whitenoise` pre-configured.

`poetry add coltrane -E deploy`
