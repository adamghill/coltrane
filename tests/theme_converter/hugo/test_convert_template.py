import pytest

from coltrane.theme_converters.hugo import convert_template_html


def test_variable():
    expected = "{{ VariableName }}"

    template_html = "{{ .VariableName }}"
    actual = convert_template_html(template_html)

    assert expected == actual


def test_block():
    expected = "{% block main %}{% endblock %}"

    template_html = '{{- block "main" . }}{{ end }}'
    actual = convert_template_html(template_html)

    assert expected == actual


def test_block_with_content():
    expected = "{% block main %}stuff in here{% endblock %}"

    template_html = '{{- block "main" . }}stuff in here{{ end }}'
    actual = convert_template_html(template_html)

    assert expected == actual


def test_comment():
    expected = "{# stuff in here #}"

    template_html = "{{* stuff in here *}}"
    actual = convert_template_html(template_html)

    assert expected == actual


def test_loop():
    expected = '{% for _ in Pages.GroupByDate|"January" %}'

    template_html = '{{- range .Pages.GroupByDate "January" }}'
    actual = convert_template_html(template_html)

    assert expected == actual


@pytest.mark.skip()
def test_base_example():
    expected = """<!DOCTYPE html>
<html lang="{% get_current_language %}" dir="auto">

<head>
    {% include "partials/head.html" %}
</head>

<body class="
{% if not request.resolver_match.url_name == 'page' or request.resolver_match.url_name in ['archives', 'search'] %}
list
{% endif %}
{% if default_theme == 'dark' %}
dark
{% endif %}
" id="top">
    {% include "partials/header.html" %}
    <main class="main">
        {% block main %}
        {% endblock %}
    </main>
    {% include "partials/footer.html" %}
</body>

</html>
"""

    template_html = """{{- if lt hugo.Version "0.112.4" }}
{{- errorf "=> hugo v0.112.4 or greater is required for hugo-PaperMod to build " }}
{{- end -}}

<!DOCTYPE html>
<html lang="{{ site.Language }}" dir="{{ .Language.LanguageDirection | default "auto" }}">

<head>
    {{- partial "head.html" . }}
</head>

<body class="
{{- if (or (ne .Kind `page` ) (eq .Layout `archives`) (eq .Layout `search`)) -}}
{{- print "list" -}}
{{- end -}}
{{- if eq site.Params.defaultTheme `dark` -}}
{{- print " dark" }}
{{- end -}}
" id="top">
    {{- partialCached "header.html" . .Page -}}
    <main class="main">
        {{- block "main" . }}{{ end }}
    </main>
    {{ partialCached "footer.html" . .Layout .Kind (.Param "hideFooter") (.Param "ShowCodeCopyButtons") -}}
</body>

</html>
"""

    actual = convert_template_html(template_html)

    assert expected == actual
