# Installation

1. Make a new directory for your site and traverse into it: `mkdir new-site && cd new-site`
1. Install `poetry` (if not already installed) to handle Python packages: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
1. Create `poetry` project, add `coltrane` dependency, and install Python packages: `poetry init --no-interaction --dependency coltrane-web:latest && poetry install`
1. Start a new `coltrane` site: `poetry run coltrane create`
1. Start local development server: `poetry run coltrane play`
1. Go to localhost:8000 in web browser
