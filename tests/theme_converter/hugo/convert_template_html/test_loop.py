from coltrane.theme_converters.hugo import convert_template_html


def test_loop():
    expected = '{% for _ in Pages.GroupByDate|"January" %}test{% endfor %}'

    template_html = '{{- range .Pages.GroupByDate "January" }}test{{ end }}'
    actual = convert_template_html(template_html)

    assert actual == expected


def test_loop_with_loop():
    expected = """{% for _ in Pages.GroupByDate|"January" %}
<div>
{% for _ in Pages.GroupByDate|"February" %}
<div></div>
{% endfor %}
</div>
{% endfor %}"""

    template_html = """{{- range .Pages.GroupByDate "January" }}
<div>
{{- range .Pages.GroupByDate "February" }}
<div></div>
{{ end }}
</div>
{{ end }}"""
    actual = convert_template_html(template_html)

    assert actual == expected
