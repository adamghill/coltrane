from copy import deepcopy
from pathlib import Path

import pytest
from django.template import TemplateSyntaxError

# from coltrane import _get_default_template_settings
from coltrane.config.settings import get_config


def test_include_md(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    # settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))
    coltrane = get_config(base_dir=tmp_path)
    settings.TEMPLATES = deepcopy(coltrane.get_templates_settings())

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

    assert (
        """<h1 id="index">index</h1>
<p><h1 id="partial">partial</h1>"""
        in actual
    )


def test_include_md_loop(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    # settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))
    coltrane = get_config(base_dir=tmp_path)
    settings.TEMPLATES = deepcopy(coltrane.get_templates_settings())

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
        """<h1 id="index">index</h1>
<p>
<h1 id="partial">partial</h1>


<h1 id="partial">partial</h1>

</p>"""
        in actual
    )


def test_include_md_metadata_in_template(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    # settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))
    coltrane = get_config(base_dir=tmp_path)
    settings.TEMPLATES = deepcopy(coltrane.get_templates_settings())

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
        """<h1 id="index">index</h1>
<p><h2 id="partial">partial</h2>
<p>this-is-a-string-in-the-template</p>
</p>"""
        in actual
    )


def test_include_md_metadata_in_partial(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    # settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))
    coltrane = get_config(base_dir=tmp_path)
    settings.TEMPLATES = deepcopy(coltrane.get_templates_settings())

    print("tmp_path", tmp_path)
    print("settings.TEMPLATES", settings.TEMPLATES)

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
    print(actual)
    assert (
        """<h1 id="index">index</h1>
<p><h2 id="partial">partial</h2>
<p>this-is-a-string-in-the-partial</p>
</p>"""
        in actual
    )


def test_include_md_no_template(client, settings, tmp_path: Path):
    settings.BASE_DIR = tmp_path
    # settings.TEMPLATES = deepcopy(_get_default_template_settings(tmp_path))
    coltrane = get_config(base_dir=tmp_path)
    settings.TEMPLATES = deepcopy(coltrane.get_templates_settings())

    (tmp_path / "content").mkdir()
    (tmp_path / "content/index.md").write_text("{% include_md %}")

    with pytest.raises(TemplateSyntaxError):
        client.get("/")
