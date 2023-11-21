# Integration

## Linking

Django templates can link to `coltrane` markdown content with the `url` template tag and the slug of the markdown file.

```html
<!-- this will link to a route which renders the /content/about.md markdown file -->
<a href="{% url 'coltrane:content' 'about' %}">About</a>
```

## Sitemap

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

More details are in [the Django documentation for sitemaps](https://docs.djangoproject.com/en/stable/ref/contrib/sitemaps/#initialization).

## RSS

RSS requires an absolute URL so `coltrane` needs to know the domain for the site. The settings file needs to include something similar to the following.

```python
COLTRANE = {
    "SITE_URL": "https://example.com",
}
```

### URL Routing

1. Add the following to `urls.py`

```python
from django.urls import path
from coltrane.feeds import ContentFeed

urlpatterns = [
    path("rss.xml", ContentFeed()),
]
```