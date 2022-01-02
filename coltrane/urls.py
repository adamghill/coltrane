from django.urls import path, re_path

from . import views


urlpatterns = [
    path("<str:slug>/", views.content),
    path("<str:slug>", views.content),
    path("", views.content),
    # re_path("", views.content),
]
