# Context

The template context for each `markdown` file includes:

- all key/value pairs in the `markdown` frontmatter
- rendered `markdown` HTML in `content`
- JSON data from the `data` directory
- `coltrane` which includes a dictionary of the [`coltrane` settings](settings.md)
- `now` which provides the current `datetime` (would be the time of HTML rendering for when generating a static site)
- `request` which provides the current request
- `debug` which contains the `DEBUG` setting (or if `INTERNAL_IPS` has the current request's IP)
- `slug` which contains the current file's "slug" (e.g. `articles/some-new-article` if there was a markdown file at `content/articles/some-new-article.md`)
- `toc` which is an automatically generated table of contents rendered as HTML
- if `publish_date` is found, it is converted to a Python `datetime` instance using the excellent [dateparser](https://dateparser.readthedocs.io/en/latest/) library

## Example context

**`data/index.json`**

```json
{ "test": "Great" }
```

**`content/index.md`**

```markdown
---
this_is_a_variable: This is a good test
template: some_app/custom-template.html
publish_date: 2022-02-26 10:26:02
---

{{ this_is_a_variable }}

Data from JSON files: {{ data.index.test }}

Current datetime: {{ now }}

Publish date: {{ publish_date|naturalday }}
```

**`some_app/templates/some_app/custom-template.html`**

```html
{{ content }}
```

**Generated `index.html`**

```html
<p>This is a good test</p>

<p>Data from JSON files: Great</p>

<p>Current datetime: 8 Jan. 11, 2022, 10:02 p.m.</p>

<p>Publish date: Feb. 26, 2022</p>
```

