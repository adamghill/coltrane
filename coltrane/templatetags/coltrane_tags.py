from typing import Dict, Union

from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.template.base import Node
from django.template.exceptions import TemplateSyntaxError
from django.template.loader_tags import construct_relative_path
from django.utils.safestring import SafeString

from coltrane.renderer import (
    get_html_and_markdown,
    render_html_with_django,
    render_markdown_path,
)
from coltrane.retriever import get_content_directory, get_content_paths


register = template.Library()


class NoParentError(Exception):
    pass


@register.simple_tag(takes_context=True)
def directory_contents(
    context, directory: str = None, exclude: str = None
) -> Dict[str, str]:
    if not directory:
        request = context["request"]
        directory = request.path
    elif isinstance(directory, SafeString):
        # Force SafeString to be a normal string so it can be used with `Path` later
        directory = directory + ""

    if directory.startswith("/"):
        directory = directory[1:]

    content_paths = get_content_paths(directory)
    contents = []

    for path in content_paths:
        if path.name != "index.md":
            path_slug = path.name[:-3]
            content_slug = path_slug
            content_directory = get_content_directory()

            if directory:
                content_slug = f"{directory}/{path_slug}"
                content_directory = content_directory / directory

            if exclude:
                if exclude.startswith("/"):
                    exclude = exclude[1:]

                if exclude == content_slug:
                    continue

            (_, metadata) = get_html_and_markdown(content_slug)

            contents.append(metadata)

    return contents


@register.filter()
def parent(path: Union[str, WSGIRequest] = "") -> str:
    if hasattr(path, "path"):
        # Handle if a `request` is passed in
        path = path.path

    path = path.strip()

    if path.endswith("/"):
        path = path[:-1]

    if path == "":
        raise NoParentError()

    last_slash_index = path.rindex("/")
    path = path[:last_slash_index]

    return path


class IncludeMarkdownNode(Node):
    """
    Based on: `django.template.loader_tags.IncludeNode`.
    """

    context_key = "__include_markdown_context"

    def __init__(self, template, *args, **kwargs):
        self.template = template
        super().__init__(*args, **kwargs)

    def render(self, context):
        """
        Render the specified template and context.
        """

        template_name = self.template.resolve(context)

        cache = context.render_context.dicts[0].setdefault(self, {})
        template = cache.get(template_name)

        if template is None:
            template = context.template.engine.select_template((template_name,))
            cache[template_name] = template

        (html, metadata) = render_markdown_path(template.origin.name)

        for c in context:
            for key, value in c.items():
                if key not in metadata:
                    metadata[key] = value

        return render_html_with_django(html, metadata)


@register.tag("include_md")
def do_include_md(parser, token):
    """
    Load a markdown template and render it with the current context.

    Based on: `django.template.loader_tags.do_include`.

    Example:
        {% include "foo/some_include" %}
    """
    bits = token.split_contents()

    if len(bits) < 2:
        raise TemplateSyntaxError(
            "%r tag takes at least one argument: the name of the template to "
            "be included." % bits[0]
        )

    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])

    return IncludeMarkdownNode(
        parser.compile_filter(bits[1]),
    )
