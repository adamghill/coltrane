# Markdown

## Rendering

`coltrane` takes the URL slug and looks up a corresponding markdown file in the `content` directory. For example: http://localhost:8000/this-is-a-good-example/ will render the markdown in `content/this-is-a-good-example.md`.

## Root

The root (i.e. http://localhost:8000/) will attempt to render the `content/index.md` file.

## Missing markdown file

If a `markdown` file cannot be found, `coltrane` will try to find a matching HTML template. If none could be found, the response will be a 404.

## Frontmatter

`YAML` before the actual `markdown` content is supported. It will be added to the context variable that is used to render the HTML. The default `base.html` template will use `lang` (to specify the HTML language; defaults to "en"), and `title` variables if they are specified in the frontmatter.

### template

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
