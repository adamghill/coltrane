from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

from coltrane.sitemaps import ContentSitemap

from . import views


app_name = "coltrane"

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

sitemaps = {"content": ContentSitemap}

urlpatterns += [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    re_path(r"^(?P<slug>(\w|-|\/)*)", views.content, name="content"),
]
