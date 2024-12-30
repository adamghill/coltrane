import importlib


def test_urlpatterns(settings):
    settings.DEBUG = False
    settings.COLTRANE["EXTRA_FILE_NAMES"] = []

    # Import module and reload it to get the right routes
    from coltrane import urls

    importlib.reload(urls)

    assert len(urls.urlpatterns) == 4

    assert urls.urlpatterns[0].pattern._route == "healthcheck"
    assert urls.urlpatterns[1].pattern._route == "sitemap.xml"
    assert urls.urlpatterns[2].pattern._route == "rss.xml"
    assert urls.urlpatterns[3].name == "content"


def test_urlpatterns_with_extra_file_names(settings):
    settings.DEBUG = False
    settings.COLTRANE["EXTRA_FILE_NAMES"] = ["robots.txt"]

    # Import module and reload it to get the right routes
    from coltrane import urls

    importlib.reload(urls)

    assert len(urls.urlpatterns) == 5

    assert urls.urlpatterns[0].pattern._route == "healthcheck"
    assert urls.urlpatterns[1].pattern._route == "sitemap.xml"
    assert urls.urlpatterns[2].pattern._route == "rss.xml"
    assert urls.urlpatterns[3].pattern._route == "robots.txt"
    assert urls.urlpatterns[4].name == "content"


def test_debug_urlpatterns(settings):
    settings.DEBUG = True
    settings.COLTRANE["EXTRA_FILE_NAMES"] = []

    # Import module and reload it to get the right routes
    from coltrane import urls

    importlib.reload(urls)

    print("urls.urlpatterns", urls.urlpatterns)

    assert len(urls.urlpatterns) == 5

    assert urls.urlpatterns[0].pattern._route == "__reload__/"
    assert urls.urlpatterns[1].pattern._route == "healthcheck"
    assert urls.urlpatterns[2].pattern._route == "sitemap.xml"
    assert urls.urlpatterns[3].pattern._route == "rss.xml"
    assert urls.urlpatterns[4].name == "content"
