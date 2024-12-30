# Changelog

## 0.38.0

- Better support for multiple domains and custom sites.
- Add `coltrane.toml` settings file.

## 0.37.0

- Automatically enable `dj-angles` if the library is installed.
- Experimental support for multiple domains.

**Breaking changes**

- Drop support for Python 3.8.
- Remove loading deprecated `data.json` file.

## 0.36.0

- Handle string, date, epoch in `publish_date` and convert them to timezone-aware datetime.

## 0.35.4

- Prevent missing `compress` templatetag from raising an error when calling the `compress` management command.

## 0.35.3

- Set `COMPRESS_OFFLINE=True` when running the `compress` management command.

## 0.35.2

- Add all environment variables to `settings.ENV`, not just the variables from `.env`.

## 0.35.1

- Update default `Dockerfile` to fix some deployment problems.

## 0.35.0

- Include variables from `.env` file in `settings.ENV`.
- Rewrite all docs to remove any perceived dependency on `poetry`.
- Create nested folder structure for new sites.

## 0.34.0

- Add `coltrane` context template variable to expose the `coltrane` settings.
- Add support for [`django-compressor`](installation.md#extras).
- Add support for [redirects](redirects.md).

## 0.33.0

- Bump `rich-click` dependency and slightly better command aliases support.

## 0.32.1

- Parse JSON5 data as UTF-8.

## 0.32.0

- Add `pubdate` to RSS feed [#61](https://github.com/adamghill/coltrane/pull/61) by [Tobi-De](https://github.com/Tobi-De).
- Support setting a custom `TIME_ZONE`.

## 0.31.0

- Create example `Dockerfile` and `gunicorn.conf.py` files for easier deployments of `coltrane` apps.
- [Add the ability](installation.md#extras) to use [JSON5](https://json5.org) for data files.

**Breaking changes**

- Remove loading `data.json`. All data should be in JSON files in the `data` directory.
- The default markdown renderer is now `mistune` instead of `markdown2`. The next version of `coltrane` will remove the option to use `markdown2`.

## 0.30.0

- Add `COLTRANE_IS_SECURE` [env variable](env.md#coltrane_is_secure).
- Add `django.middleware.gzip.GZipMiddleware`, `django.middleware.http.ConditionalGetMiddleware`, `django.middleware.csrf.CsrfViewMiddleware` middlewares.

## 0.29.0

- [`django-unicorn`](https://www.django-unicorn.com) integration.
- Fix: Passing `INSTALLED_APPS` into `init` now does not override the default apps.

## 0.28.0

- Add `DISABLE_WILDCARD_TEMPLATES` setting.
- Add `data`, `slug`, `template`, and `now` to direct HTML template for as much parity to `markdown` content as possible.

## 0.27.0

- Support directory wildcards.
- Add `paths` template tag.

## 0.26.0

- Ability to [configure cache](env.md#cache).
- Allow content or data directory to be specified [#48](https://github.com/adamghill/coltrane/issues/48).
- Fix: Handle invalid JSON data [#48](https://github.com/adamghill/coltrane/issues/48).

## 0.25.0

- If a markdown file with a slug cannot be found, look for a template with the same slug. Special case for `*.html` which can be a fall-back option to render for any slug.
- Add `raise_404` template tag.
- Add `last_path` template tag.

## 0.24.0

- Support Django template tags with the `mistune` markdown renderer.

## 0.23.1

- Include extra files when building the static site.

## 0.23.0

- Add `EXTRA_FILE_NAMES` setting to support serving static files like `robots.txt`.

## 0.22.0

- Add support for rendering markdown with `mistune`. See [MARKDOWN_RENDERED](settings.md) for how to enable. `mistune` will be the default renderer after 0.22.0 because it is 1) faster rendering markdown than `markdown2`, 2) enables new functionality like `abbr`, 3) fixed a bug in the generation of the tables of contents HTML, and 4) has a plugin architecture to add new features.
- Improve table of contents rendering for `mistune`.

## 0.21.0

- Add `order_by` to `directory_contents` templatetag.
- Fix `TOC` outputting 'None' when it should be `None`.

## 0.20.0

- Add `to_html` template tag. [#37](https://github.com/adamghill/coltrane/pull/37) by [Tobi-De](https://github.com/Tobi-De)
- Breaking change: change `date` to `publish_date` in metadata. [#39](https://github.com/adamghill/coltrane/pull/37) by [Tobi-De](https://github.com/Tobi-De)
- Breaking change: change `SITE` setting to `SITE_URL`.
- Automatically add `verbatim` templatetag around code fences.

## 0.19.0

- Update project name to `coltrane`.

## 0.18.3

- Fix bug where templatetags could not be loaded when the base directory was ".".

## 0.18.2

- Add `request` to the template context when building static sites.

## 0.18.1

- Fix bug where static site path was incorrect.

## 0.18.0

- Add `toc` to the template context which provides a table of contents for the markdown.

## 0.17.0

- Fix bug with relative URLs when generating `sitemap.xml`
- Automatic generation of `rss.xml` file

## 0.16.1

- Create `COLTRANE_SITE` setting in `.env` file during `create` command

## 0.16.0

- Output an error if rendering fails during `record` command
- `include_md` template tag
- `parent` filter
- Serving of `/sitemap.xml` for standalone
- Automatic creation of `sitemap.xml` during `record` command

**Breaking changes**

- `COLTRANE_SITE` is required in .env file

## 0.15.1

- Include all frontmatter metadata in `directory_contents` template tag output
- Parse `date` frontmatter into `datetime`
- Parse `draft` frontmatter into `boolean`

## 0.15.0

- [`directory_contents`](template-tags.md) template tag
- Add [`django-fastdev`](https://github.com/boxed/django-fastdev) for more immediate feedback when an invalid template variable is used
- Show error message if a markdown file cannot be output to HTML
- Fix bug where `index.md` files in a sub-directory were not output correctly

## 0.14.0

- Add `--output` option to `record` command [#19](https://github.com/adamghill/coltrane/issues/19) by [stlk](https://github.com/stlk)
- Nicer help output for CLI

## 0.13.1

- Add `--threads` option to `record` command

## 0.13.0

- Multithread `record` command
- Better console output for `record` command

## 0.12.0

- Fix elapsed time for `record` command
- More performant collection of markdown content files
- Don't include markdown or data when collecting static files while running `record`

## 0.11.0

- Add `--force` option to `create` command
- Automatically refresh the browser when markdown content or data is saved

## 0.10.0

- Fix generating root `index.md`

## 0.9.0

- Add support for static files
- Add `watchman` support
- Add `whitenoise` for static handling
- Add `--force` option to `record` command

## 0.8.0

- Read `INTERNAL_IPS` from .env file
- Add `now` to template variables
- Include found template tags in built-ins
- Include `humanize` template tags in built-ins

## 0.7.0

- Support nested directories for content and data
- Update default markdown extras

## 0.6.0

- Add support for markdown frontmatter
- Support custom templates specified in markdown frontmatter

## 0.5.0

- Add `build` maangement command
- Store build manifest so that HTML doesn't re-render if possible
- Loosen dependencies

## 0.4.0

- Unit tests, coverage, and fixes for mypy

## 0.3.0

- Bug fixes

## 0.2.0

- Bug fixes

## 0.1.0

- Basic Django app which renders markdown files at a URL
- Basic script
