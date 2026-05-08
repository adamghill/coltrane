import importlib

from django.test import Client

from coltrane.config.settings import reset_config_cache


def test_redirects_toml(settings, tmp_path):
    # Setup tmp directory as BASE_DIR
    settings.BASE_DIR = tmp_path
    (tmp_path / "coltrane.toml").write_text("""
[coltrane]

[[redirects]]
from_url = "/test-redirect"
to_url = "/"
""")

    # Reset config cache to ensure the new TOML is loaded
    reset_config_cache()

    # Reload urls not strictly necessary for views logic change,
    # but good to ensure clean state if any other internal caching exists
    from coltrane import urls

    importlib.reload(urls)

    client = Client()
    response = client.get("/test-redirect")

    assert response.status_code == 302
    assert response.url == "/"


def test_site_specific_redirects(settings, tmp_path):
    settings.BASE_DIR = tmp_path

    # Create sites structure
    (tmp_path / "sites" / "site1").mkdir(parents=True)
    (tmp_path / "sites" / "site2").mkdir(parents=True)

    (tmp_path / "coltrane.toml").write_text("""
[coltrane]

[[sites]]
folder = "site1"
hosts = ["site1.com"]
[[sites.redirects]]
from_url = "/foo"
to_url = "/bar"

[[sites]]
folder = "site2"
hosts = ["site2.com"]
[[sites.redirects]]
from_url = "/foo"
to_url = "/baz"

[[redirects]]
from_url = "/global"
to_url = "/global-target"
""")

    reset_config_cache()
    from coltrane import urls

    importlib.reload(urls)

    client = Client()

    # Test Site 1
    response = client.get("/foo", headers={"host": "site1.com"})
    assert response.status_code == 302
    assert response.url == "/bar"

    # Test Site 2
    response = client.get("/foo", headers={"host": "site2.com"})
    assert response.status_code == 302
    assert response.url == "/baz"

    # Test Global Redirect on Site 1
    response = client.get("/global", headers={"host": "site1.com"})
    assert response.status_code == 302
    assert response.url == "/global-target"
