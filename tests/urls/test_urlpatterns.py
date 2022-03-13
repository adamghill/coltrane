import importlib

from coltrane import urls


def test_urlpatterns():
    importlib.reload(urls)
    assert len(urls.urlpatterns) == 3


def test_debug_urlpatterns(settings):
    settings.DEBUG = True
    importlib.reload(urls)

    assert len(urls.urlpatterns) == 4
