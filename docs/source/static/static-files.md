# Static Files

Django has a process for handling static files (i.e. files like CSS, SASS, JavaScript, images) already which `coltrane` leverages as part of the [record CLI command](static/cli.md#record). The `collectstatic` management command is used to copy all static files from different Django apps to the `output/static` directory.

## Referring to static assets

Instead of hardcoding the URL path to static assets, the `static` templatetag is always available in either markdown files or templates.

```{note}
Using the `static` template tag might feel unnecessary for simpler sites, but it will automatically use the hashed file name that `whitenoise` provides for efficient serving and caching of static files.
```

**`content/index.md`**

```markdown
![music note]({% static 'images/music-note.svg' %})
```

**Generated `index.html`**

```html
<img src="/static/images/music-note.abcd123.svg" />
```

**`templates/custom/custom-template.html`**

```html
<link src='{% static 'css/styles.css' %}'>
```

**Generated HTML**

```html
<link src="/static/css/styles.wxyz789.css" />
```
