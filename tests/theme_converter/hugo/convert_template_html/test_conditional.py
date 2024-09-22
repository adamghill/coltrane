from coltrane.theme_converters.hugo import convert_template_html


def test_if():
    expected = """{% if Description %}
<div class="post-description">
    {{ Description }}
</div>
{% endif %}"""

    template_html = """{{- if .Description }}
<div class="post-description">
    {{ .Description }}
</div>
{{- end }}"""
    actual = convert_template_html(template_html)

    assert actual == expected


def test_if_else():
    expected = """{% if Description %}
<div class="post-description">
    {{ Description }}
</div>
{% endif %}"""

    template_html = """{{- if .Description }}
<div class="post-description">
    {{ .Description }}
</div>
{{- end }}"""
    actual = convert_template_html(template_html)

    assert actual == expected
