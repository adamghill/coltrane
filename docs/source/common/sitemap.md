# Sitemap

Django provides a built-in way to create a `sitemap.xml` for search engines to find content on your site. `Coltrane` automatically creates a `sitemap.xml` when building a static site and has a URL route for it for a standalone site. However, for integrated sites, you will need to configure the sitemap to use `Coltrane` to build the file.

## Integrated mode installation

1. Add `"django.contrib.sitemaps",` to `INSTALLED_APPS` in the settings file
1. Make sure your `TEMPLATES` setting contains a `DjangoTemplates` backend whose `APP_DIRS` options is set to `True`.
1. Add the following to `urls.py`

```python
from django.contrib.sitemaps.views import sitemap
from coltrane.sitemaps import ContentSitemap

# Make sure that the protocol is https
ContentSitemap.protocol = "https"

sitemaps = {
    "content": ContentSitemap,
}

urlpatterns = [
    # other URL paths here
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # other URL paths here
]
```

More details are in [the Django documentation for sitemaps](https://docs.djangoproject.com/en/stable/ref/contrib/sitemaps/#initialization). Although, note that the `sites` framework is *not* a hard requirement for the `sites.xml` file to be created.
