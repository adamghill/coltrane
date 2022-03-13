from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

from coltrane.feeds import ContentFeed
from coltrane.sitemaps import ContentSitemap

from . import views


app_name = "coltrane"

sitemaps = {"content": ContentSitemap}

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

urlpatterns += [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("rss.xml", ContentFeed()),
    re_path(r"^(?P<slug>(\w|-|\/)*)", views.content, name="content"),
]
