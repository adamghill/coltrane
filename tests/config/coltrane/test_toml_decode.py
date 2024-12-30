import msgspec

from coltrane.config.coltrane import Config


def test_empty():
    data = b""

    actual = msgspec.toml.decode(data, type=Config)

    assert actual
    assert len(actual.redirects) == 0
    assert len(actual.sites) == 1

    default_site = actual.sites[0]
    assert default_site.folder == ""
    assert len(default_site.hosts) == 1
    assert default_site.hosts[0] == "*"


def test_redirects():
    data = b"""
[[redirects]]
from_url = "/test-1" 
to_url = "/"
permanent = false

[[redirects]]
from_url = "/test-2"
to_url = "/"
"""

    actual = msgspec.toml.decode(data, type=Config)

    assert actual
    assert actual.redirects
    assert len(actual.redirects) == 2


def test_sites():
    data = b"""
[[sites]]
folder = "adamghill"
hosts = [
  "0.0.0.0:80",
  "0.0.0.0:8020",
  "localhost:8020",
  "adamghill.localhost",
  "adamghill.com"
]

[[sites]]
folder = "alldjango"
hosts = [
  "0.0.0.0:8021",
  "localhost:8021",
  "alldjango.localhost",
  "alldjango.com"
]
"""

    actual = msgspec.toml.decode(data, type=Config)

    assert actual
    assert actual.sites
    assert len(actual.sites) == 2

    site_0 = actual.sites[0]
    assert site_0.folder == "adamghill"
    assert len(site_0.hosts) == 5

    site_1 = actual.sites[1]
    assert site_1.folder == "alldjango"
    assert len(site_1.hosts) == 4
