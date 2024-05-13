# Introduction

`coltrane` is a [**Dynamic Site Generator**](index.md#-what-is-a-dynamic-site-generator). It can be used as a self-contained app for content sites, as a third-party app in a `Django` project to render `markdown` files, or to build a static HTML website.

## ⭐ Features

- Render `markdown` files as HTML with automatic URL routing based on the filesystem
- Local development server with live re-rendering of markdown and data
- Use JSON files as a data source
- Automatic generation of `sitemap.xml` and `rss.xml`
- Can also serve non-markdown files, e.g. `robots.txt`
- Site-wide redirects
- Deployment best practices with `Docker`, `whitenoise`, and `gunicorn` already pre-configured
- Leverage built-in or custom `Django` template tags and filters
- Include any third-party [`Django` app](https://djangopackages.org) for additional functionality
- Optional building of static HTML files

## 🙋 What is a Dynamic Site Generator?

`coltrane` is similar to a static site generator -- it takes `markdown` content and renders it as HTML. However, it also provides an opinionated framework for building dynamic websites.

### Examples in the wild

- [GitEgo](https://adamghill.com/gitego): An egocentric view of GitHub (uses the GitHub GraphQL endpoints)
- [python-utils](https://adamghill.com/python-utils): Interactive Python playground (uses `django-unicorn` component library)
- [unsuckjs.com](https://unsuckjs.com): Libraries to progressively enhance HTML with minimal amounts of JavaScript (uses GitHub REST API)
- [djangobrew.com](https://djangobrew.com): Website for the Django Brew podcast (uses the Buzzsprout API)

```{note}
Please [let me know](https://github.com/adamghill/coltrane/discussions/new?category=show-and-tell) if you use `coltrane` and would like to add it to this list!
```

## 🎵 What's with the name?

`coltrane` is built on top of the `Django` web framework, which is named after [Django Reinhardt](https://en.wikipedia.org/wiki/Django_Reinhardt). This framework is named after [John Coltrane](https://en.wikipedia.org/wiki/John_Coltrane), another (more avant-garde 🎶) jazz musician.

## 🙏 Inspiration

https://twitter.com/willmcgugan/status/1477283879841157123 for the initial inspiration and my reaction https://twitter.com/adamghill/status/1477414858396164096.

## ⚙️ Dependencies

- https://github.com/adamchainz/django-browser-reload for development server live reloads
- https://github.com/boxed/django-fastdev to ensure template variables are available
- https://github.com/lepture/mistune for doing the hard work of rendering the markdown
- https://www.djangoproject.com for doing the hard work of everything else

## 🎉 Other minimal `Django` projects

- https://github.com/wsvincent/django-microframework for the `app.py` idea
- https://olifante.blogs.com/covil/2010/04/minimal-django.html
- https://simonwillison.net/2009/May/19/djng/
- https://stackoverflow.com/questions/1297873/how-do-i-write-a-single-file-django-application
- https://github.com/pauloxnet/uDjango

## 🧠 Related projects

[yamdl](https://github.com/andrewgodwin/yamdl) is another approach which lets you store instances of Django models as flat YAML files. It also supports storing markdown.

Here are a few Python static site generators:
- [Pelican](https://getpelican.com/): Pelican is a static site generator that requires no database or server-side logic.
- [Combine](https://combine.dropseed.dev/): Build a straightforward marketing or documentation website with the power of Jinja.
- [Nikola](https://getnikola.com/): In goes content, out comes a website, ready to deploy.
- [Lektor](https://www.getlektor.com/): A flexible and powerful static content management system for building complex and beautiful websites out of flat files.
- [corvid](https://github.com/di/corvid): An opinionated simple static site generator.
- [jamstack](https://github.com/Abdur-RahmaanJ/jamstack): The easiest way to create jamstack sites, as simple or as complex as you like.

```{toctree}
:maxdepth: 2
:hidden:

self
installation
local-development
content
```

```{toctree}
:caption: Features
:maxdepth: 2
:hidden:

templates
template-tags
context
data
static-files
sitemap
redirects
rss
deployment
```

```{toctree}
:caption: Misc
:maxdepth: 2
:hidden:

cli
env
settings
```

```{toctree}
:caption: Static Site Generator
:maxdepth: 2
:hidden:

static-site-generator/build
```

```{toctree}
:caption: Django App
:maxdepth: 2
:hidden:

django-app/installation
django-app/integration
```

```{toctree}
:caption: Info
:maxdepth: 2
:hidden:

changelog
GitHub <https://github.com/adamghill/coltrane>
Sponsor <https://github.com/sponsors/adamghill>
```
