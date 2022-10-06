from pathlib import Path
from unittest.mock import call, patch

from coltrane.renderer import RenderedMarkdown


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

    (tmp_path / "content").mkdir()
    (tmp_path / "content/dir").mkdir()
    (tmp_path / "content/dir/index.md").write_text("# dir")

    response = client.get("/dir/")
    assert response.status_code == 200

    actual = response.content.decode()
    assert '<h1 id="dir">dir</h1>' in actual


def test_directory_index_without_slash(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content/dir").mkdir()
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


def test_url_slug_with_data(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-this-data.md").write_text("test data {{ data.test }}")
    (tmp_path / "data.json").write_text('{"test":1}')

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
        return_value=(RenderedMarkdown("coltrane/content.html", context)),
    ) as _get_from_cache_if_enabled:
        with patch(
            "coltrane.views._set_in_cache_if_enabled"
        ) as _set_in_cache_if_enabled:
            response = client.get("/test-this-cache")
            assert response.status_code == 200
            assert response.headers.get("Cache-Control") == "max-age=15"
            assert response.headers.get("Expires")
            original_expires = response.headers.get("Expires")

            # Call view again
            response = client.get("/test-this-cache")
            assert response.status_code == 200
            assert response.headers.get("Expires") == original_expires

            _get_from_cache_if_enabled.assert_has_calls(
                calls=[call("test-this-cache"), call("test-this-cache")]
            )
            _set_in_cache_if_enabled.assert_not_called()
