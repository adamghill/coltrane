# Static Files

`Django` handles static files (e.g. CSS, JavaScript, and images) already which `coltrane` leverages as part of the [record command](cli.md#record). The [`collectstatic` management command](https://docs.djangoproject.com/en/stable/ref/contrib/staticfiles/#collectstatic) is used to copy all static files to the `output/static` directory.

## Referring to static assets

Instead of hardcoding the URL path to static assets, the `static` template tag should be used in either `markdown` or HTML templates.

```{note}
Using the `static` template tag might feel unnecessary for simpler sites, but it will automatically use hashed file names that `whitenoise` provides for efficient serving and caching of static files.
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
<link src="{% static 'css/styles.css' %}" />
```

**Generated HTML**

```html
<link src="/static/css/styles.wxyz789.css" />
```
