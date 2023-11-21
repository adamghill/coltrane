<p align="center">
  <a href="https://coltrane.readthedocs.io"><h1 align="center">coltrane</h1></a>
</p>
<p align="center">A Dynamic Site Generator that harnesses the power of Django without the hassle 🎵</p>

![PyPI](https://img.shields.io/pypi/v/coltrane?color=blue&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/coltrane?color=blue&style=flat-square)
![GitHub Sponsors](https://img.shields.io/github/sponsors/adamghill?color=blue&style=flat-square)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

📖 Complete documentation at https://coltrane.readthedocs.io.

📦 Package located at https://pypi.org/project/coltrane/.

## ⭐ Features

- Render `markdown` files as HTML with automatic URL routing based on the filesystem
- Use JSON files as data sources in HTML templates or `markdown`
- Automatic generation of `sitemap.xml` and `rss.xml` files
- Can serve non-markdown files like `robots.txt`
- Local development server which includes [live re-rendering of markdown and data](https://twitter.com/adamghill/status/1487522925393715205) via https://github.com/adamchainz/django-browser-reload
- Deployment best practices with `whitenoise` and `gunicorn` already configured
- Leverage the power of built-in `Django` templates, template tags, and filters inside markdown files
- Any custom template tags and filters are enabled automatically for use in `markdown` or HTML templates
- Include any third-party [`Django` app](https://djangopackages.org) for additional functionality
- Optional static site generator to output HTML files
- Able to be integrated into a regular `Django` project as a third-party `Django` app

## ⚡ Quick start

1. `mkdir new-site && cd new-site` to create a new folder
1. `poetry init --no-interaction --dependency 'coltrane:<1' && poetry install` to create a new virtual environment and install the `coltrane` package
1. Optional: `brew install watchman` on MacOS for less resource-intensive local development server
1. `poetry run coltrane create` to create the folder structure for a new site
1. `poetry run coltrane play` to start local development server
1. Go to http://localhost:8000 to see the original markdown rendered into HTML
1. Update `content/index.md`
1. Go to http://localhost:8000 to see the updated markdown rendered into HTML
1. Optional: run `poetry run coltrane record` to build static HTML files

### Generated `coltrane` file structure

```bash
.
├── __init__.py
├── app.py
├── content
│   └── index.md
├── data
├── poetry.lock
└── pyproject.toml
```

## 📝 Content

Add `markdown` files or sub-directories to the `content` directory and rendered HTML will be accessible via auto-generated routes.

- `/` would render the `markdown` in `content/index.md`
- `/about/` would render the `markdown` in `content/about.md`
- `/articles/this-is-the-first-article/` would render the content from `/content/articles/this-is-the-first-article.md`
- `/not-there/` will 404

HTML will also be served automatically if a `markdown` file can not be found.

- `/app/` would render the HTML from `/templates/app.html` or `/templates/app/index.html`
- `/app/some-user` would render the HTML from `/templates/app/*.html`

# 📖 Documentation

Read all of the documentation at https://coltrane.readthedocs.io.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/Tobi-De"><img src="https://avatars.githubusercontent.com/u/40334729?v=4?s=100" width="100px;" alt="Tobi DEGNON"/><br /><sub><b>Tobi DEGNON</b></sub></a><br /><a href="https://github.com/adamghill/coltrane/commits?author=Tobi-De" title="Tests">⚠️</a> <a href="https://github.com/adamghill/coltrane/commits?author=Tobi-De" title="Code">💻</a></td>
    </tr>
  </tbody>
  <tfoot>
    
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
