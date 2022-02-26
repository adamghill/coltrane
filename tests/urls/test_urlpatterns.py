import importlib

from coltrane import urls


def test_urlpatterns_has_2():
    assert len(urls.urlpatterns) == 2


def test_debug_urlpatterns_has_3(settings):
    settings.DEBUG = True
    importlib.reload(urls)

    assert len(urls.urlpatterns) == 3
