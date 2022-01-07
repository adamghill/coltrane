from pathlib import Path

from django.conf import settings


def test_404(client):
    response = client.get("/")
    assert response.status_code == 404


def test_index(client, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "index.md").write_text("# index")

    response = client.get("/")
    assert response.status_code == 200

    actual = response.content.decode()
    assert '\n<h1 id="index">index</h1>\n\n' in actual


def test_url_slug(client, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-this.md").write_text("# test this")

    response = client.get("/test-this")
    assert response.status_code == 200

    actual = response.content.decode()
    assert '\n<h1 id="test-this">test this</h1>\n\n' in actual


def test_url_slug_with_data(client, tmp_path: Path):
    settings.BASE_DIR = tmp_path

    (tmp_path / "content").mkdir()
    (tmp_path / "content" / "test-this-data.md").write_text("test data {{ data.test }}")
    (tmp_path / "data.json").write_text('{"test":1}')

    response = client.get("/test-this-data")
    assert response.status_code == 200

    actual = response.content.decode()
    assert "\n<p>test data 1</p>\n\n" in actual
