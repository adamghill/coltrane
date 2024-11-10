from coltrane.views import _get_potential_wildcard_templates, _sort_potential_templates


def test_get_potential_wildcard_templates():
    expected = [
        "*.html",
    ]

    slug = "test"
    actual = _get_potential_wildcard_templates(slug)

    assert actual == expected


def test_get_potential_wildcard_templates_sub_directory():
    expected = ["test/*.html", "*/this.html", "*/*.html"]

    slug = "test/this"
    actual = _get_potential_wildcard_templates(slug)

    assert actual == expected


def test_get_potential_wildcard_templates_sub_directories():
    expected = [
        "test/this/*.html",
        "test/*/now.html",
        "*/this/now.html",
        "test/*/*.html",
        "*/this/*.html",
        "*/*/*.html",
    ]

    slug = "test/this/now"
    actual = _get_potential_wildcard_templates(slug)

    assert actual == expected


def test_sort_potential_templates():
    expected = [
        "test/this/*.html",
        "test/*/now.html",
        "test/*/*.html",
        "*/this/now.html",
        "*/this/*.html",
        "*/*/*.html",
    ]

    actual = _sort_potential_templates(
        [
            "*/*/*.html",
            "test/*/*.html",
            "*/this/now.html",
            "test/this/*.html",
            "*/this/*.html",
            "test/*/now.html",
        ]
    )

    assert actual == expected
