from django.conf import settings
from django.urls import include, path, re_path

from . import views


app_name = "coltrane"

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

urlpatterns += [
    re_path(r"^(?P<slug>(\w|-|\/)*)", views.content, name="content"),
]
