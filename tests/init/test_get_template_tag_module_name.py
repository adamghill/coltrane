from pathlib import Path

from django.template.library import InvalidTemplateLibrary

import pytest

from coltrane import _get_template_tag_module_name


def test_get_template_tag_module_name():
    expected = "example_standalone.templatetags.custom_tags"
    actual = _get_template_tag_module_name(
        Path("../example_standalone"),
        Path("example_standalone/templatetags/custom_tags.py"),
    )

    assert actual == expected


def test_get_template_tag_module_name():
    with pytest.raises(InvalidTemplateLibrary):
        _get_template_tag_module_name(
            Path("../example_standalone"),
            Path("example_standalone/templatetags/custom_tags"),
        )


def test_get_template_tag_module_name_invalid():
    with pytest.raises(InvalidTemplateLibrary):
        _get_template_tag_module_name(
            Path("../example_standalone"),
            Path("example_standalone/templatetags/custom_tags2.py"),
        )
