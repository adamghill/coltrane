# Introduction

`coltrane` is a content site framework that harnesses the power of Django without the hassle. It can be used to generate a static site for easy serving of HTML files or as an opinionated Django package to render markdown.

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

## Installation

Because `coltrane` can be used in a few different ways, the documentation is split into different sections.

- [static site](static/index)
- [simplified standalone Django project](standalone/index)
- [integrated into an existing Django project](integrated/index)

### Optional installation

- Enable `watchman` for less resource-intensive autoreload on MacOS: `brew install watchman`

## What's with the name?

`coltrane` is built on top of the Django web framework, which is named after [Django Reinhardt](https://en.wikipedia.org/wiki/Django_Reinhardt). Following in that tradition, I named this static site framework after [John Coltrane](https://en.wikipedia.org/wiki/John_Coltrane), another jazz musician.

## Related projects

There are a ton of other static site generators out there. Here are a few Python static site generators in case it's useful.

- [Pelican](https://getpelican.com/): Pelican is a static site generator that requires no database or server-side logic
- [Combine](https://combine.dropseed.dev/): Build a straightforward marketing or documentation website with the power of Jinja. No fancy JavaScript here — this is just like the good old days
- [Nikola](https://getnikola.com/): In goes content, out comes a website, ready to deploy.
- [Lektor](https://www.getlektor.com/): A flexible and powerful static content management system for building complex and beautiful websites out of flat files
- [corvid](https://github.com/di/corvid): An opinionated simple static site generator
- [jamstack](https://github.com/Abdur-RahmaanJ/jamstack): The easiest way to create jamstack sites, as simple or as complex as you like

## Inspiration and thanks

- https://twitter.com/willmcgugan/status/1477283879841157123 for the initial inspiration and my reaction: https://twitter.com/adamghill/status/1477414858396164096

### Dependencies

- https://github.com/trentm/python-markdown2 for doing the hard work of rendering the markdown
- https://www.djangoproject.com for doing the hard work of everything else

### Minimal Django projects

- https://github.com/wsvincent/django-microframework for the `app.py` idea
- https://olifante.blogs.com/covil/2010/04/minimal-django.html
- https://simonwillison.net/2009/May/19/djng/
- https://stackoverflow.com/questions/1297873/how-do-i-write-a-single-file-django-application

```{toctree}
:maxdepth: 2
:hidden:

self
```

```{toctree}
:caption: Static Site
:maxdepth: 2
:hidden:

static/index
static/installation
static/cli
static/hosting
```

```{toctree}
:caption: Standalone Site
:maxdepth: 2
:hidden:

standalone/index.md
standalone/installation
standalone/serve
```

```{toctree}
:caption: Integrated Site
:maxdepth: 2
:hidden:

integrated/index
integrated/installation
integrated/integration
```

```{toctree}
:caption: Common
:maxdepth: 2
:hidden:

common/markdown
common/templates
common/context
common/data
common/static-files
common/sitemap
common/rss
common/settings
common/env
```

```{toctree}
:maxdepth: 2
:hidden:

GitHub <https://github.com/adamghill/coltrane>
Sponsor <https://github.com/sponsors/adamghill>
```
