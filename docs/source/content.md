# Content

`coltrane` is designed around content. There are no URL routes to configure or `views` (if you are used to Django) or `controllers` (if you are used to other MVC frameworks) to create. `coltrane` automatically routes URLs to the correct content based on where the files exist on the filesystem. `markdown` files will get converted to HTML for rendering. HTML template files can also be served directly for more control.

## Markdown

Add `markdown` files (or sub-directories with `markdown` files) to the `content` directory and rendered HTML will be accessible via auto-generated routes. `index.md` would be used similarly to `index.html`.

- `/` would convert the `markdown` in `content/index.md` and render is as HTML
- `/about/` would convert the `markdown` in `content/about.md` and render it as HTML
- `/articles/` would convert the `markdown` in `/content/articles/index.md` and render it as HTML
- `/articles/this-is-the-first-article/` would convert the `markdown` in `/content/articles/this-is-the-first-article.md` and render it as HTML
- `/not-there/` would 404

### Frontmatter

`YAML` before the actual `markdown` content is supported. Any keys and their values will be added to the `context` variable that is used when rendering the HTML. The default `base.html` template will use `lang` (to specify the HTML language; defaults to "en"), and `title` variables if they are specified in the frontmatter.

#### template

Used to specify a custom template that Django will use to render the `markdown`.

**`content/index.md`**

```markdown
---
lang: en
title: This is a good title
template: another_app/new-template.html
adjective: perfect
---

This is sample text
```

**`another_app/new-template.html`**

```html
<title>{{ title }}</title>

{{ content }} and it's {{ adjective }}
```

**Generated HTML**

```html
<title>This is a good title</title>

<p>This is sample text and it's perfect</p>
```

## HTML

If a `markdown` file can not be found for the based on the URL's `slug`, but there is an HTML file with the same `slug` in the `templates` directory the HTML template will be rendered.

- `/app/` would render the HTML in `/templates/app.html` or `/templates/app/index.html`

### Wildcards

A filename with an asterisk can be used as a "wildcard" and will be served for any `slug` that does not have a matching `markdown` or specific HTML template file.

- `/app/some-user` would render the HTML from `/templates/app/*.html`

Directories can also be a wildcard to handle a specific part of a slug.

- `/app/some-user` would render the HTML from (in priority order) `/templates/app/some-user.html` or `/templates/app/*.html` or `/templates/*/some-user.html` or `/templates/*/*.html`
- `/app/another-user` would render the HTML from (in priority order) `/templates/app/another-user.html` or `/templates/app/*.html` or `/templates/*/another-user.html` or `/templates/*/*.html`
