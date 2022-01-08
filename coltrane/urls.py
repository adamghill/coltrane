from django.urls import re_path

from . import views


app_name = "coltrane"

urlpatterns = [
    re_path(r"^(?P<slug>(\w|-|\/)*)", views.content, name="content"),
]
