from copy import deepcopy
from pathlib import Path
from unittest.mock import call, patch

from coltrane.config.settings import get_config


def _setup_settings(settings, tmp_path: Path) -> None:
    settings.BASE_DIR = tmp_path

    config = get_config()
    assert config.has_custom_sites is False

    # Set Django templates settings
    settings.TEMPLATES = deepcopy(config.get_templates_settings())


def test_404(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()

    response = client.get("/")
    assert response.status_code == 404


def test_404_directory_parent_traversal(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()

    response = client.get("/../")
    assert response.status_code == 404


def test_404_directory_home_traversal(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    (tmp_path / "content").mkdir()

    response = client.get("/../")
    assert response.status_code == 404


def test_index_with_slash(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "index.md").write_text("# index")

    response = client.get("/")
    assert response.status_code == 200

    actual = response.content.decode()
    assert '<h1 id="index">index</h1>' in actual


def test_index_without_slash(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "index.md").write_text("# index")

    response = client.get("")
    assert response.status_code == 200

    actual = response.content.decode()
    assert '<h1 id="index">index</h1>' in actual


def test_directory_index_with_slash(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content/dir").mkdir(parents=True)
    (tmp_path / "content/dir/index.md").write_text("# dir")

    response = client.get("/dir/")
    assert response.status_code == 200

    actual = response.content.decode()
    assert '<h1 id="dir">dir</h1>' in actual


def test_directory_index_without_slash(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content/dir").mkdir(parents=True)
    (tmp_path / "content/dir/index.md").write_text("# dir")

    response = client.get("/dir")
    assert response.status_code == 200

    actual = response.content.decode()
    assert '<h1 id="dir">dir</h1>' in actual


def test_url_slug(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-this.md").write_text("# test this")

    response = client.get("/test-this")
    assert response.status_code == 200

    actual = response.content.decode()
    assert '\n<h1 id="test-this">test this</h1>\n\n' in actual


def test_url_slug_with_json_data(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-this-data.md").write_text("test data {{ data.test }}")
    (tmp_path / "data").mkdir()
    (tmp_path / "data/test.json").write_text("1")

    response = client.get("/test-this-data")
    assert response.status_code == 200

    actual = response.content.decode()
    assert "\n<p>test data 1</p>\n\n" in actual


def test_url_slug_with_json5_data(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-this-data.md").write_text("test data {{ data.test }}")
    (tmp_path / "data").mkdir()
    (tmp_path / "data/test.json5").write_text("1")

    response = client.get("/test-this-data")
    assert response.status_code == 200

    actual = response.content.decode()
    assert "\n<p>test data 1</p>\n\n" in actual


def test_url_slug_cache_headers(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.COLTRANE = {"VIEW_CACHE": {"SECONDS": 15}}

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-this-cache.md").write_text("test cache")

    response = client.get("/test-this-cache")
    assert response.status_code == 200
    assert response.headers.get("Cache-Control") == "max-age=15"
    assert response.headers.get("Expires")
    original_expires = response.headers.get("Expires")

    # Call view again
    response = client.get("/test-this-cache")
    assert response.status_code == 200
    assert response.headers.get("Expires") == original_expires


def test_url_slug_cache(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.COLTRANE = {"VIEW_CACHE": {"SECONDS": 15}}

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-this-cache.md").write_text("test cache")

    context = {
        "template": "coltrane/content.html",
        "data": {},
        "content": "<p>test cache</p>\n",
    }

    with patch(
        "coltrane.views._get_from_cache_if_enabled",
        return_value=("coltrane/content.html", context),
    ) as _get_from_cache_if_enabled:
        with patch("coltrane.views._set_in_cache_if_enabled") as _set_in_cache_if_enabled:
            response = client.get("/test-this-cache")
            assert response.status_code == 200
            assert response.headers.get("Cache-Control") == "max-age=15"
            assert response.headers.get("Expires")
            original_expires = response.headers.get("Expires")

            # Call view again
            response = client.get("/test-this-cache")
            assert response.status_code == 200
            assert response.headers.get("Expires") == original_expires

            _get_from_cache_if_enabled.assert_has_calls(calls=[call("test-this-cache"), call("test-this-cache")])
            _set_in_cache_if_enabled.assert_not_called()


def test_url_slug_direct_template(client, settings, tmp_path: Path):
    _setup_settings(settings, tmp_path)

    (tmp_path / "templates").mkdir(parents=True)
    (tmp_path / "templates" / "test-this.html").write_text("test this")

    response = client.get("/test-this")
    assert response.status_code == 200

    actual = response.content.decode()
    assert "test this" in actual


def test_url_slug_direct_template_wildcard(client, settings, tmp_path: Path):
    _setup_settings(settings, tmp_path)

    (tmp_path / "templates").mkdir(parents=True)
    (tmp_path / "templates" / "*.html").write_text("asterisk")

    response = client.get("/test-this-missing-thing")
    assert response.status_code == 200

    actual = response.content.decode()
    assert "asterisk" in actual


def test_url_wildcards(client, settings, tmp_path: Path):
    _setup_settings(settings, tmp_path)

    (tmp_path / "templates" / "test-this").mkdir(parents=True)
    (tmp_path / "templates" / "test-this" / "*.html").write_text("directory asterisk")

    response = client.get("/test-this/missing-thing")
    assert response.status_code == 200

    actual = response.content.decode()
    assert "directory asterisk" in actual


def test_url_wildcards_404(client, settings, tmp_path: Path):
    _setup_settings(settings, tmp_path)

    (tmp_path / "templates").mkdir(parents=True)
    (tmp_path / "templates" / "*.html").write_text("multiple asterisk")

    response = client.get("/something/test-this-should-404")
    assert response.status_code == 404


def test_url_multiple_wildcards(client, settings, tmp_path: Path):
    _setup_settings(settings, tmp_path)

    (tmp_path / "templates" / "*").mkdir(parents=True)
    (tmp_path / "templates" / "*" / "*.html").write_text("multiple asterisk")

    response = client.get("/something/test-this-should-200")
    assert response.status_code == 200

    actual = response.content.decode()
    assert "multiple asterisk" in actual


def test_url_multiple_wildcards_and_multiple_subdirectories(client, settings, tmp_path: Path):
    _setup_settings(settings, tmp_path)

    (tmp_path / "templates" / "new" / "another" / "*").mkdir(parents=True)
    (tmp_path / "templates" / "new" / "another" / "*" / "*.html").write_text("multiple asterisk in subdirectory")

    response = client.get("/new/another/something/test-this-should-200")
    assert response.status_code == 200

    actual = response.content.decode()
    assert "multiple asterisk in subdirectory" in actual


def test_include(client, settings, tmp_path: Path):
    _setup_settings(settings, tmp_path)

    (settings.BASE_DIR / "templates").mkdir(parents=True)
    (settings.BASE_DIR / "templates/_partial.html").write_text("""
This is a partial
""")
    (settings.BASE_DIR / "templates/include-1.html").write_text("""
template 1

{% include '_partial.html' %}
""")

    response = client.get("/include-1")

    assert response.status_code == 200

    actual = response.content.decode()
    assert "This is a partial" in actual


def test_static(client, settings, tmp_path: Path):
    _setup_settings(settings, tmp_path)

    text = """
static 1

<img src="{% static 'img/example.png' %}" />
"""
    (settings.BASE_DIR / "templates").mkdir(parents=True)
    (settings.BASE_DIR / "templates/static-1.html").write_text(text)

    actual = client.get("/static-1")

    assert 200 == actual.status_code
    assert '<img src="static/img/example.png" />' in actual.content.decode()
