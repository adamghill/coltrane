# Context

The template context for each markdown file rendered by `coltrane` includes:

- all variables from the markdown frontmatter
- rendered markdown HTML in `content`
- JSON data from the `data` directory
- `now` which provides the current `datetime` (would be the time of HTML rendering for static site)
- `request` which provides the current request for an integrated or standalone site
- `debug` which contains the the `DEBUG` setting for an integrated or standalone site (if `INTERNAL_IPS` has the current request's IP which is usually `127.0.0.1` for local development)
- `slug` which contains the current file's "slug" (e.g. `articles/some-new-article` if there was a markdown file at `content/articles/some-new-article.md`)
- `toc` which is an automatically generated table of contents rendered as HTML

**`data/index.json`**

```json
{ "test": "Great" }
```

**`content/index.md`**

```markdown
---
this_is_a_variable: This is a good test
template: some_app/custom-template.html
---

{{ this_is_a_variable }}

Data from JSON files: {{ data.index.test }}

Current datetime: {{ now }}
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
```

