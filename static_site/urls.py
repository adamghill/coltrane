from django.urls import path

from . import views

urlpatterns = [
    path("<str:slug>/", views.content),
    path("<str:slug>", views.content),
    path("", views.content),
]
