<p align="center">
  <a href="https://coltrane.readthedocs.io"><h1 align="center">coltrane</h1></a>
</p>
<p align="center">A simple content site framework that harnesses the power of Django without the hassle 🎵</p>

![PyPI](https://img.shields.io/pypi/v/coltrane-web?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/coltrane-web?color=blue&style=flat-square)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)

📖 Complete documentation: https://coltrane.readthedocs.io

📦 Package located at https://pypi.org/project/coltrane-web/

## ⭐ Features

- Can either generate a static HTML, be used as a standalone Django site, or integrated into an existing Django site
- Write content in markdown and render it in HTML
- Use data from JSON files in templates and content
- All the power of Django templates, template tags, and filters
- Can include other Django apps for additional functionality
- Opinionated Django project setup where everything works "out of the box"

## ⚡ Quick start for a new static site

1. `mkdir new-site && cd new-site` to create a new folder
1. `poetry init --no-interaction --dependency 'coltrane-web:<1' && poetry install` to create a new virtual environment and install the `coltrane` package
1. `poetry run coltrane create` to create the folder structure for a new site
1. Update `content/index.md`
1. `poetry run coltrane play` for a local development server
1. Go to http://localhost:8000 to see the updated markdown rendered into HTML
1. `poetry run coltrane record` to output the rendered HTML files

## Optional

- Enable `watchman` for less resource-intensive autoreload on Mac: `brew install watchman`

## How to add new content

Add markdown files or sub-directories with msrkdown files to the `content` directory and they will automatically have routes created that can be requested.

With this folder structure:

```
/content/index.md
/content/about.md
/content/articles/this-is-the-first-article.md
```

There will be these URLs available:

- `http://localhost:8000/` which serves HTML generated from the `/content/index.md` file
- `http://localhost:8000/about` which serves HTML generated from the `/content/about.md` file
- `http://localhost:8000/articles/this-is-the-first-article` which serves HTML generated from the `/content/articles/this-is-the-first-article.md` file

Read all of the documentation at https://coltrane.readthedocs.io.
