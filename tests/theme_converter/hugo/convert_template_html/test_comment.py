from coltrane.theme_converters.hugo import convert_template_html


def test_comment():
    expected = "{# stuff in here #}"

    template_html = "{{* stuff in here *}}"
    actual = convert_template_html(template_html)

    assert actual == expected
