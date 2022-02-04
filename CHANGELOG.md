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
