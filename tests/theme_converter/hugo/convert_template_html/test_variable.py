from coltrane.theme_converters.hugo import convert_template_html


def test_variable():
    expected = "{{ VariableName }}"

    template_html = "{{ .VariableName }}"
    actual = convert_template_html(template_html)

    assert actual == expected
