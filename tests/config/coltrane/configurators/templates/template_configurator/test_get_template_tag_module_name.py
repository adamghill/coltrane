from pathlib import Path

import pytest
from django.template.library import InvalidTemplateLibrary

from coltrane.config.coltrane.configurators.templates import TemplatesConfigurator
from coltrane.config.settings import get_config


def get_templates_configurator(path: str) -> TemplatesConfigurator:
    coltrane = get_config(base_dir=Path(path))

    return TemplatesConfigurator(coltrane)


def test_get_template_tag_module_name():
    expected = "example_standalone.templatetags.custom_tags"

    templates_configurator = get_templates_configurator("../example_standalone")
    actual = templates_configurator._get_template_tag_module_name(
        Path("example_standalone/templatetags/custom_tags.py")
    )

    assert actual == expected


def test_get_template_tag_module_name_invalid_missing_extension():
    templates_configurator = get_templates_configurator("../example_standalone")

    with pytest.raises(InvalidTemplateLibrary):
        templates_configurator._get_template_tag_module_name(Path("../example_standalone"))


def test_get_template_tag_module_name_invalid_wrong_file():
    templates_configurator = get_templates_configurator("../example_standalone")

    with pytest.raises(InvalidTemplateLibrary):
        templates_configurator._get_template_tag_module_name(
            Path("example_standalone/templatetags/custom_tags2.py"),
        )


def test_get_template_tag_module_name_with_period_base_dir():
    expected = "example_standalone.templatetags.custom_tags"

    templates_configurator = get_templates_configurator(".")
    actual = templates_configurator._get_template_tag_module_name(
        Path("example_standalone/templatetags/custom_tags.py"),
    )

    assert actual == expected
