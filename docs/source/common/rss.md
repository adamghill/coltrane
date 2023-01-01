# RSS

Coltrane will automatically create an `rss.xml` file or path with all of the content. In standalone mode, it will be served from the `/rss.xml` path. For static mode, the `rss.xml` file will be created in the build directory.

## Required setting

Because RSS requires an absolute URL, `coltrane` needs to know about the current domain for the site.

For static or standalone mode, `COLTRANE_SITE_URL` needs to be set in the `.env` file. For integrated mode, the settings file requires something like the following.

```python
COLTRANE = {
    "SITE_URL": "https://example.com",
}
```

## Integrated mode installation

1. Add the following to `urls.py`

```python
from django.urls import path
from coltrane.feeds import ContentFeed

urlpatterns = [
    path("rss.xml", ContentFeed()),
]
```