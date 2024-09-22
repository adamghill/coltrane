from coltrane.theme_converters.hugo import convert_template_html


def test_block():
    expected = "{% block main %}{% endblock %}"

    template_html = '{{- block "main" . }}{{ end }}'
    actual = convert_template_html(template_html)

    assert actual == expected


def test_block_with_content():
    expected = "{% block main %}test block{% endblock %}"

    template_html = '{{- block "main" . }}test block{{ end }}'
    actual = convert_template_html(template_html)

    assert actual == expected
