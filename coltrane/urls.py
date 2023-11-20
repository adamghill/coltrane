from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path

from coltrane import views
from coltrane.config.settings import get_extra_file_names
from coltrane.feeds import ContentFeed
from coltrane.sitemaps import ContentSitemap

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
]

# Add file names to serve to url routes (e.g. robots.txt)
for file_name in get_extra_file_names():
    urlpatterns += [
        path(file_name, views.file, kwargs={"file_name": file_name}),
    ]

# Add catch-all route for markdown content
urlpatterns += [
    re_path(r"^(?P<slug>(\w|-|\/)*)", views.content, name="content"),
]
