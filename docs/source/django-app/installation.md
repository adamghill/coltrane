# Installation

1. `pip install coltrane` (or use whatever Python package manager you like)
1. Add `coltrane` to the list of `INSTALLED_APPS` in Django settings file
1. Add `path("", include("coltrane.urls")),` to the bottom of the `urlpatterns` in the root `urls.py` (i.e. the `urls.py` specified by `ROOT_URLCONF`)

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    ...
    path("", include("coltrane.urls")),
]
```
