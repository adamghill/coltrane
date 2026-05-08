from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.template.base import Node, SafeString
from django.template.exceptions import TemplateSyntaxError
from django.template.loader_tags import construct_relative_path, do_extends, do_include
from django.templatetags.static import StaticNode
from django.utils.safestring import mark_safe

from coltrane.config.settings import get_config
from coltrane.renderer import MarkdownRenderer
from coltrane.retriever import get_content_directory, get_content_paths

register = template.Library()


class NoParentError(Exception):
    pass


def _is_content_slug_in_string(content_slug: str, slugs: str | None) -> bool:
    """
    Whether a content slug is included in a string. Handles if `string` is
    comma-delimited list of slugs. Also handles any individual slug
    to check having a forward-slash prefix.
    """

    if not slugs:
        return False

    if not isinstance(slugs, str):
        raise TypeError("Slugs must be a string")

    split_slugs = slugs.split(",")

    for slug in split_slugs:
        slug_to_check = slug.strip()

        if slug_to_check.startswith("/"):
            slug_to_check = slug_to_check[1:]

        if slug_to_check == content_slug:
            return True

    return False


@register.simple_tag(takes_context=True)
def directory_contents(
    context, directory: str | None = None, exclude: str | None = None, order_by=None
) -> list[dict[str, str]]:
    """
    Returns a list of content metadata for a particular directory. Useful for
    listing links to content.
    """

    request = context["request"]

    site = get_config().get_site(request)

    if not directory:
        directory = request.path
    elif isinstance(directory, SafeString):
        # Force SafeString to be a normal string so it can be used with `Path` later
        directory = directory + ""

    if directory and directory.startswith("/"):
        directory = directory[1:]

    content_paths = get_content_paths(request, str(directory))
    contents = []

    for path in content_paths:
        if path.name != "index.md":
            path_slug = path.name[:-3]
            content_slug = path_slug
            content_directory = get_content_directory()

            if directory:
                content_slug = f"{directory}/{path_slug}"
                content_directory = content_directory / directory

            if _is_content_slug_in_string(content_slug=content_slug, slugs=exclude):
                continue

            (_, metadata) = MarkdownRenderer.instance().get_html_and_markdown(content_slug, site)

            contents.append(metadata)

    if order_by and contents:
        is_reverse = False

        if order_by[0] == "-":
            is_reverse = order_by[0] == "-"
            order_by = order_by[1:]

        def _directory_content_sorter(_metadata: dict) -> str:
            value = _metadata.get(order_by, "") or ""

            return str(value)

        contents.sort(key=_directory_content_sorter, reverse=is_reverse)

    return contents


@register.filter(name="parent")
def parent(path: str | WSGIRequest = "") -> str:
    """
    Gets the the directory above `path`.
    """

    if isinstance(path, WSGIRequest) or hasattr(path, "path"):
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

        # If the current request is for a custom site, target that site's template folder
        if request := context.get("request"):
            template_name = get_config().get_site(request).get_template_name(template_name, verify=False)

        cache = context.render_context.dicts[0].setdefault(self, {})
        template = cache.get(template_name)

        if template is None:
            template = context.template.engine.select_template((template_name,))
            cache[template_name] = template

        (html, metadata) = MarkdownRenderer.instance().render_markdown_path(template.origin.name)

        for c in context:
            for key, value in c.items():
                if key not in metadata:
                    metadata[key] = value

        return MarkdownRenderer.instance().render_html_with_django(html, metadata)


@register.tag("include_md")
def do_include_md(parser, token):
    """
    Load a markdown template and render it with the current context.

    Based on: `django.template.loader_tags.do_include`.

    Example:
        {% include_md "foo/some_include" %}
    """

    bits = token.split_contents()

    if len(bits) < 2:  # noqa: PLR2004
        raise TemplateSyntaxError(
            f"{bits[0]!r} tag takes at least one argument: the name of the template to be included."
        )

    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])

    return IncludeMarkdownNode(
        parser.compile_filter(bits[1]),
    )


class TemplateNameWrapper:
    """
    A wrapper for a template name (usually a `FilterExpression`) that resolves
    to a site-specific template name if a request is in the context.
    """

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def resolve(self, context, ignore_failures=False):
        template_name = self.wrapped.resolve(context, ignore_failures)

        if isinstance(template_name, str | SafeString):
            if request := context.get("request"):
                template_name = get_config().get_site(request).get_template_name(template_name, verify=False)

        return template_name

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


@register.tag("site_include")
def do_site_include(parser, token):
    """
    Load a template and render it with the current context. You can pass
    additional context using keyword arguments.

    Example:
        {% site_include "foo/some_include" %}
        {% site_include "foo/some_include" with bar="BAZZ!" baz="BING!" %}

    Use the `only` argument to exclude the current context when rendering
    the included template::

        {% site_include "foo/some_include" only %}
        {% site_include "foo/some_include" with bar="1" only %}
    """

    node = do_include(parser, token)
    node.template = TemplateNameWrapper(node.template)

    return node


@register.filter(name="to_html", is_safe=True)
def to_html(text: str) -> str:
    """
    Convert markdown to HTML.
    """

    (html, metadata) = MarkdownRenderer.instance().render_markdown_text(text)
    rendered_html = MarkdownRenderer.instance().render_html_with_django(html, metadata)

    return mark_safe(rendered_html)  # noqa: S308


@register.simple_tag
def raise_404(message: str | None = None):
    """Raise a 404 with an optional message."""

    if message:
        raise Http404(message)

    raise Http404()


@register.simple_tag(takes_context=True)
def last_path(context: dict) -> str:
    """Return the last part of the `HTTPRequest` path.

    For example, if `request.path` is "/something/cool", "cool" would be returned.
    """

    request = context["request"]
    path = request.path_info.strip()

    if path.endswith("/"):
        path = path[:-1]

    return path.split("/")[-1:][0]


@register.simple_tag(takes_context=True)
def paths(context: dict) -> list[str]:
    """Return all parts of the `HTTPRequest` path.

    For example, if `request.path` is "/something/cool", ["something", "cool"] would be returned.
    """

    request = context["request"]
    path = request.path_info.strip()

    if path.startswith("/"):
        path = path[1:]

    if path.endswith("/"):
        path = path[:-1]

    _paths = path.split("/")

    if _paths == [""]:
        _paths = []

    return _paths


class SiteStaticNode(StaticNode):
    """Used for the custom static templatetag which knows how to deal with per-site static directory. Using
    the typical Django static template tag would require having nested directories in every static directory
    to prevent different sites from using the incorrect file.

    Allows this directory structure:
    - /sites/site1/static/styles.css
    - /sites/site2/static/styles.css

    Instead of requiring namespacing static files inside each static directory:
    - /sites/site1/static/site1/styles.css
    - /sites/site2/static/site2/styles.css
    """

    def url(self, context):
        path = self.path.resolve(context)

        if "request" in context:
            request = context["request"]

            coltrane = get_config()
            site = coltrane.get_site(request)

            path = f"static/{path}"

            if site.is_custom:
                path = f"{site.folder}/{path}"

        return self.handle_simple(path)


@register.tag("site_static")
def do_site_static(parser, token):
    """
    Coltrane's static templatetag.

    Join the given path with the STATIC_URL setting.

    Usage::

        {% site_static path [as varname] %}

    Examples::

        {% site_static "myapp/css/base.css" %}
        {% site_static variable_with_path %}
        {% site_static "myapp/css/base.css" as admin_base_css %}
        {% site_static variable_with_path as varname %}
    """

    return SiteStaticNode.handle_token(parser, token)


@register.tag("site_extends")
def do_site_extends(parser, token):
    """
    Signal that this template extends a parent template.

    This tag may be used in two ways: ``{% site_extends "base" %}`` (with quotes)
    uses the literal value "base" as the name of the parent template to extend,
    or ``{% site_extends variable %}`` uses the value of ``variable`` as either the
    name of the parent template to extend (if it evaluates to a string) or as
    the parent template itself (if it evaluates to a Template object).
    """

    node = do_extends(parser, token)
    node.parent_name = TemplateNameWrapper(node.parent_name)

    return node
