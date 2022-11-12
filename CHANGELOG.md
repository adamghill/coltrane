# 0.20.0

- Add `to_html` template tag. [#37](https://github.com/adamghill/coltrane/pull/37) by [Tobi-De](https://github.com/Tobi-De)
- Breaking change: change `date` to `publish_date` in metadata. [#39](https://github.com/adamghill/coltrane/pull/37) by [Tobi-De](https://github.com/Tobi-De)
- Breaking change: change `SITE` setting to `SITE_URL`.
- Automatically add `verbatim` templatetag around code fences.

# 0.19.0

- Update project name to `coltrane`.

# 0.18.3

- Fix bug where templatetags could not be loaded when the base directory was ".".

# 0.18.2

- Add `request` to the template context when building static sites.

# 0.18.1

- Fix bug where static site path was incorrect.

# 0.18.0

- Add `toc` to the template context which provides a table of contents for the markdown.

# 0.17.0

- Fix bug with relative URLs when generating `sitemap.xml`
- Automatic generation of `rss.xml` file

# 0.16.1

- Create `COLTRANE_SITE` setting in `.env` file during `create` command

# 0.16.0

- Output an error if rendering fails during `record` command
- `include_md` template tag
- `parent` filter
- Serving of `/sitemap.xml` for standalone
- Automatic creation of `sitemap.xml` during `record` command

_Breaking changes_

- `COLTRANE_SITE` is required in .env file

# 0.15.1

- Include all frontmatter metadata in `directory_contents` template tag output
- Parse `date` frontmatter into `datetime`
- Parse `draft` frontmatter into `boolean`

# 0.15.0

- [`directory_contents`](templates#coltrane-template-tags) template tag
- Add [`django-fastdev`](https://github.com/boxed/django-fastdev) for more immediate feedback when an invalid template variable is used
- Show error message if a markdown file cannot be output to HTML
- Fix bug where `index.md` files in a sub-directory were not output correctly

# 0.14.0

- Add `--output` option to `record` command [#19](https://github.com/adamghill/coltrane/issues/19) by [stlk](https://github.com/stlk)
- Nicer help output for CLI

# 0.13.1

- Add `--threads` option to `record` command

# 0.13.0

- Multithread `record` command
- Better console output for `record` command

# 0.12.0

- Fix elapsed time for `record` command
- More performant collection of markdown content files
- Don't include markdown or data when collecting static files while running `record`

# 0.11.0

- Add `--force` option to `create` command
- Automatically refresh the browser when markdown content or data is saved

# 0.10.0

- Fix generating root `index.md`

# 0.9.0

- Add support for static files
- Add `watchman` support
- Add `whitenoise` for static handling
- Add `--force` option to `record` command

# 0.8.0

- Read `INTERNAL_IPS` from .env file
- Add `now` to template variables
- Include found template tags in built-ins
- Include `humanize` template tags in built-ins

# 0.7.0

- Support nested directories for content and data
- Update default markdown extras

# 0.6.0

- Add support for markdown frontmatter
- Support custom templates specified in markdown frontmatter

# 0.5.0

- Add `build` maangement command
- Store build manifest so that HTML doesn't re-render if possible
- Loosen dependencies

# 0.4.0

- Unit tests, coverage, and fixes for mypy

# 0.3.0

- Bug fixes

# 0.2.0

- Bug fixes

# 0.1.0

- Basic Django app which renders markdown files at a URL
- Basic script
