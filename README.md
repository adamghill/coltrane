<p align="center">
  <a href="https://coltrane.readthedocs.io"><h1 align="center">coltrane</h1></a>
</p>
<p align="center">A simple content site framework that harnesses the power of Django without the hassle 🎵</p>

![PyPI](https://img.shields.io/pypi/v/coltrane?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/coltrane?color=blue&style=flat-square)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)

📖 Complete documentation: https://coltrane.readthedocs.io

📦 Package located at https://pypi.org/project/coltrane/

## ⭐ Features

- Can either generate a static HTML site, be deployed as a standalone Django site, or integrated into an existing Django site
- Reads markdown content and renders it in HTML
- Can use data from JSON files in templates and markdown content
- Automatic generation of `sitemap.xml` and `rss.xml` files
- [Live re-rendering of markdown and data](https://twitter.com/adamghill/status/1487522925393715205) when markdown or JSON data files are saved with the magic of https://github.com/adamchainz/django-browser-reload
- All the power of Django templates, template tags, and filters inside markdown files
- Can include other Django apps for additional functionality
- Custom Template tags are supported and are enabled automatically for use in markdown content
- Opinionated standalone Django project setup where deployment (including static files) just works "out of the box"

## ⚡ Quick start for a new static site

1. `mkdir new-site && cd new-site` to create a new folder
1. `poetry init --no-interaction --dependency 'coltrane:<1' && poetry install` to create a new virtual environment and install the `coltrane` package
1. `poetry run coltrane create` to create the folder structure for a new site
1. Update `content/index.md`
1. `poetry run coltrane play` for a local development server
1. Go to http://localhost:8000 to see the updated markdown rendered into HTML
1. `poetry run coltrane record` to output the rendered HTML files

### Optional installation

- Enable `watchman` for less resource-intensive autoreload on MacOS: `brew install watchman`

## ➕ How to add new content

Add markdown files or sub-directories with markdown files to the `content` directory and they will automatically have routes created that can be requested.

**Example markdown files**

```
content/index.md
content/about.md
content/articles/this-is-the-first-article.md
```

**`poetry run coltrane play` will serve these URLs**

- `http://localhost:8000/` which serves HTML generated from the `/content/index.md` file
- `http://localhost:8000/about/` which serves HTML generated from the `/content/about.md` file
- `http://localhost:8000/articles/this-is-the-first-article/` which serves HTML generated from the `/content/articles/this-is-the-first-article.md` file
- `http://localhost:8000/not-there/` will 404

**`poetry run coltrane record` will create these HTML files for a static site**

- `output/index.html`
- `output/about/index.html`
- `output/articles/this-is-the-first-article/index.html`

Read all of the documentation at https://coltrane.readthedocs.io.
