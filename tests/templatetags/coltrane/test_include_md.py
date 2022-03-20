from copy import deepcopy
from pathlib import Path

from django.template import TemplateSyntaxError

import pytest

from coltrane import _get_default_template_settings


def test_include_md(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))

    (tmp_path / "templates").mkdir()
    (tmp_path / "templates/_partial.md").write_text("# partial")

    (tmp_path / "content").mkdir()
    (tmp_path / "content/index.md").write_text(
        """
# index

{% include_md '_partial.md' %}
"""
    )

    response = client.get("/")
    assert response.status_code == 200

    actual = response.content.decode()
    assert '<h1 id="index">index</h1>\n\n<p><h1 id="partial">partial</h1>' in actual


def test_include_md_loop(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))

    (tmp_path / "templates").mkdir()
    (tmp_path / "templates/_partial.md").write_text("# partial")

    (tmp_path / "content").mkdir()
    (tmp_path / "content/index.md").write_text(
        """
# index

{% for i in '01'|make_list %}
{% include_md '_partial.md' %}
{% endfor %}
"""
    )

    response = client.get("/")
    assert response.status_code == 200

    actual = response.content.decode()
    assert (
        '<h1 id="index">index</h1>\n\n<p>\n<h1 id="partial">partial</h1>\n\n\n<h1 id="partial">partial</h1>'
        in actual
    )


def test_include_md_metadata_in_template(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))

    (tmp_path / "templates").mkdir()
    (tmp_path / "templates/_partial.md").write_text(
        """
## partial

{{ variable }}

"""
    )

    (tmp_path / "content").mkdir()
    (tmp_path / "content/index.md").write_text(
        """---
variable: this-is-a-string-in-the-template
---

# index

{% include_md '_partial.md' %}
"""
    )

    response = client.get("/")
    assert response.status_code == 200

    actual = response.content.decode()
    assert (
        '<h1 id="index">index</h1>\n\n<p><h2 id="partial">partial</h2>\n\n<p>this-is-a-string-in-the-template'
        in actual
    )


def test_include_md_metadata_in_partial(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))

    (tmp_path / "templates").mkdir()
    (tmp_path / "templates/_partial.md").write_text(
        """---
request: this-is-a-string-in-the-partial
---

## partial

{{ request }}

"""
    )

    (tmp_path / "content").mkdir()
    (tmp_path / "content/index.md").write_text(
        """
# index

{% include_md '_partial.md' %}
"""
    )

    response = client.get("/")
    assert response.status_code == 200

    actual = response.content.decode()
    assert (
        '<h1 id="index">index</h1>\n\n<p><h2 id="partial">partial</h2>\n\n<p>this-is-a-string-in-the-partial'
        in actual
    )


def test_include_md_no_template(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))

    (tmp_path / "content").mkdir()
    (tmp_path / "content/index.md").write_text("{% include_md %}")

    with pytest.raises(TemplateSyntaxError):
        client.get("/")
