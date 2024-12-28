from copy import deepcopy
from pathlib import Path

from coltrane.config.settings import get_config


def _get_coltrane_toml() -> str:
    return """
[coltrane]

[[sites]]
folder = "example"
hosts = [
  "example.com"
]
"""


def _setup_sites_settings(settings, tmp_path: Path) -> None:
    settings.BASE_DIR = tmp_path / "sites"

    settings.BASE_DIR.mkdir()
    (settings.BASE_DIR / "coltrane.toml").write_text(_get_coltrane_toml())

    config = get_config()
    assert config.has_custom_sites

    # Set Django templates settings
    settings.TEMPLATES = deepcopy(config.get_templates_settings())


def _write_text(path: Path, text: str):
    (path.parent).mkdir(parents=True)
    (path).write_text(text)


def _client_get(client, url, headers: dict | None = None):
    if headers is None:
        headers = {"X-Forwarded-Host": "example.com"}

    return client.get(url, headers=headers)


def test_404(client, settings, tmp_path: Path):
    _setup_sites_settings(settings, tmp_path)

    response = _client_get(client, "/")

    assert response.status_code == 404


def test_index_md(client, settings, tmp_path: Path):
    _setup_sites_settings(settings, tmp_path)

    (settings.BASE_DIR / "example/content").mkdir(parents=True)
    (settings.BASE_DIR / "example/content/index.md").write_text("# index md")

    response = _client_get(client, "/")

    assert response.status_code == 200

    actual = response.content.decode()
    assert '<h1 id="index-md">index md</h1>' in actual


def test_md_without_slash(client, settings, tmp_path: Path):
    _setup_sites_settings(settings, tmp_path)

    (settings.BASE_DIR / "example/content").mkdir(parents=True)
    (settings.BASE_DIR / "example/content/test-md-1.md").write_text("# test md 1")

    response = _client_get(client, "/test-md-1")

    assert response.status_code == 200

    actual = response.content.decode()
    assert '<h1 id="test-md-1">test md 1</h1>' in actual


def test_md_with_slash(client, settings, tmp_path: Path):
    _setup_sites_settings(settings, tmp_path)

    (settings.BASE_DIR / "example/content").mkdir(parents=True)
    (settings.BASE_DIR / "example/content/test-md-2.md").write_text("# test md 2")

    response = _client_get(client, "/test-md-2/")

    assert response.status_code == 200

    actual = response.content.decode()
    assert '<h1 id="test-md-2">test md 2</h1>' in actual


def test_template_without_slash(client, settings, tmp_path: Path):
    _setup_sites_settings(settings, tmp_path)

    (settings.BASE_DIR / "example/templates").mkdir(parents=True)
    (settings.BASE_DIR / "example/templates/test-template-1.html").write_text("Test template 1")

    response = _client_get(client, "/test-template-1")

    assert response.status_code == 200

    actual = response.content.decode()
    assert "Test template 1" == actual


def test_template_with_slash(client, settings, tmp_path: Path):
    _setup_sites_settings(settings, tmp_path)

    (settings.BASE_DIR / "example/templates").mkdir(parents=True)
    (settings.BASE_DIR / "example/templates/test-template-2.html").write_text("Test template 2")

    response = _client_get(client, "/test-template-2/")

    assert response.status_code == 200

    actual = response.content.decode()
    assert "Test template 2" == actual


def test_md_with_template(client, settings, tmp_path: Path):
    _setup_sites_settings(settings, tmp_path)

    (settings.BASE_DIR / "example/content").mkdir(parents=True)
    (settings.BASE_DIR / "example/content/test-md-with-template.md").write_text("""
---
template: template-1.html
---

# test md with template
""")

    (settings.BASE_DIR / "example/templates").mkdir(parents=True)
    (settings.BASE_DIR / "example/templates/template-1.html").write_text("""
template 1

{{ content }}
""")

    response = _client_get(client, "/test-md-with-template")

    assert response.status_code == 200

    actual = response.content.decode()
    assert "template 1" in actual
    assert '<h1 id="test-md-with-template">test md with template</h1>' in actual


def test_include(client, settings, tmp_path: Path):
    _setup_sites_settings(settings, tmp_path)

    (settings.BASE_DIR / "example/templates").mkdir(parents=True)
    (settings.BASE_DIR / "example/templates/_partial.html").write_text("""
This is a partial
""")
    (settings.BASE_DIR / "example/templates/include-1.html").write_text("""
template 1

{% include '_partial.html' %}
""")

    response = _client_get(client, "/include-1")

    assert response.status_code == 200

    actual = response.content.decode()
    assert "This is a partial" in actual


def test_static(client, settings, tmp_path: Path):
    _setup_sites_settings(settings, tmp_path)

    text = """
static 1

<img src="{% static 'img/example.png' %}" />
"""
    _write_text(settings.BASE_DIR / "example/templates/static-1.html", text)

    actual = _client_get(client, "/static-1")

    assert 200 == actual.status_code
    assert '<img src="example/static/img/example.png" />' in actual.content.decode()
