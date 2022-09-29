# RSS

Coltrane will automatically create an `rss.xml` file or path with all of the content. In integrated or standalone mode, it will be served from the `/rss.xml` path. For static mode, the `rss.xml` file will be created in the build directory.

## Required Setting

Because RSS requires an absolute URL, `coltrane` needs to know about the current domain for the site.

For integrated or standalone mode, `COLTRANE_SITE` needs to be set in the `.env` file. For integrated mode, the settings file requires something like the following.

```python
COLTRANE = {
    "SITE": "https://example.com",
}
```
