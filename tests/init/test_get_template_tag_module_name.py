from pathlib import Path

import pytest
from django.template.library import InvalidTemplateLibrary

from coltrane import _get_template_tag_module_name


def test_get_template_tag_module_name():
    expected = "example_standalone.templatetags.custom_tags"
    actual = _get_template_tag_module_name(
        Path("../example_standalone"),
        Path("example_standalone/templatetags/custom_tags.py"),
    )

    assert actual == expected


def test_get_template_tag_module_name_invalid_missing_extension():
    with pytest.raises(InvalidTemplateLibrary):
        _get_template_tag_module_name(
            Path("../example_standalone"),
            Path("example_standalone/templatetags/custom_tags"),
        )


def test_get_template_tag_module_name_invalid_wrong_file():
    with pytest.raises(InvalidTemplateLibrary):
        _get_template_tag_module_name(
            Path("../example_standalone"),
            Path("example_standalone/templatetags/custom_tags2.py"),
        )


def test_get_template_tag_module_name_with_period_base_dir():
    expected = "example_standalone.templatetags.custom_tags"
    actual = _get_template_tag_module_name(
        Path("."),
        Path("example_standalone/templatetags/custom_tags.py"),
    )

    assert actual == expected
