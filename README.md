# coltrane

A simple content site framework that harnesses the power of Django without the hassle.

## 🎵 Features

- Can either generate a static HTML, be used as a standalone Django site, or integrated into an existing Django site
- Write content in markdown and render it in HTML
- Use data from JSON files in templates and content
- All the power of Django templates, template tags, and filters
- Can include other Django apps for additional functionality
- Opinionated Django project setup where everything works "out of the box"

## ⚡ Quick start for a new static site

1. `mkdir new-site && cd new-site` to create a new folder
1. `poetry init --no-interaction --dependency coltrane-web:latest && poetry install` to create a new virtual environment and install `coltrane`
1. `poetry run coltrane create` to create the folder structure for a new site
1. Update `content/index.md`
1. `poetry run coltrane play` for a local development server
1. Go to http://localhost:8000 to see the updated markdown rendered into HTML
1. `poetry run coltrane record` to output the rendered HTML files

📖 Complete documentation: https://coltrane.readthedocs.io.

📦 Package located at https://pypi.org/project/coltrane-web/.
