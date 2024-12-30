from typing import Dict, List, Optional, Union

from django import template
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.template.base import Node, Template, TextNode, token_kwargs
from django.template.exceptions import TemplateSyntaxError
from django.template.loader_tags import BLOCK_CONTEXT_KEY, BlockContext, BlockNode, construct_relative_path
from django.templatetags.static import StaticNode
from django.utils.safestring import SafeString, mark_safe

from coltrane.config.settings import get_config
from coltrane.renderer import MarkdownRenderer
from coltrane.retriever import get_content_directory, get_content_paths

register = template.Library()


class NoParentError(Exception):
    pass


def _is_content_slug_in_string(content_slug: str, slugs: Optional[str]) -> bool:
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
    context, directory: Optional[str] = None, exclude: Optional[str] = None, order_by=None
) -> List[Dict[str, str]]:
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

        def _directory_content_sorter(_metadata: Dict) -> str:
            value = _metadata.get(order_by, "") or ""

            return str(value)

        contents.sort(key=_directory_content_sorter, reverse=is_reverse)

    return contents


@register.filter()
def parent(path: Union[str, WSGIRequest] = "") -> str:
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
            "%r tag takes at least one argument: the name of the template to be included." % bits[0]
        )

    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])

    return IncludeMarkdownNode(
        parser.compile_filter(bits[1]),
    )


class IncludeNode(Node):
    context_key = "__include_context"

    def __init__(self, template, *args, extra_context=None, isolated_context=False, **kwargs):
        self.template = template
        self.extra_context = extra_context or {}
        self.isolated_context = isolated_context
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}: template={self.template!r}>"

    def render(self, context):
        """
        Render the specified template and context. Cache the template object
        in render_context to avoid reparsing and loading when used in a for
        loop.
        """

        template = self.template.resolve(context)

        if isinstance(template, str) or isinstance(template, SafeString):
            if request := context.get("request"):
                template = get_config().get_site(request).get_template_name(template)

        # Does this quack like a Template?
        if not callable(getattr(template, "render", None)):
            # If not, try the cache and select_template().
            template_name = template or ()

            if isinstance(template_name, str):
                template_name = (
                    construct_relative_path(
                        self.origin.template_name,
                        template_name,
                    ),
                )
            else:
                template_name = tuple(template_name)

            cache = context.render_context.dicts[0].setdefault(self, {})
            template = cache.get(template_name)

            if template is None:
                template = context.template.engine.select_template(template_name)
                cache[template_name] = template

        # Use the base.Template of a backends.django.Template.
        elif hasattr(template, "template"):
            template = template.template

        values = {name: var.resolve(context) for name, var in self.extra_context.items()}

        if self.isolated_context:
            return template.render(context.new(values))

        with context.push(**values):
            return template.render(context)


@register.tag("include")
def do_include(parser, token):
    """
    Load a template and render it with the current context. You can pass
    additional context using keyword arguments.

    Example:
        {% include "foo/some_include" %}
        {% include "foo/some_include" with bar="BAZZ!" baz="BING!" %}

    Use the `only` argument to exclude the current context when rendering
    the included template::

        {% include "foo/some_include" only %}
        {% include "foo/some_include" with bar="1" only %}
    """

    bits = token.split_contents()

    if len(bits) < 2:
        raise TemplateSyntaxError(
            "%r tag takes at least one argument: the name of the template to be included." % bits[0]
        )

    options = {}
    remaining_bits = bits[2:]

    while remaining_bits:
        option = remaining_bits.pop(0)

        if option in options:
            raise TemplateSyntaxError("The %r option was specified more than once." % option)
        if option == "with":
            value = token_kwargs(remaining_bits, parser, support_legacy=False)

            if not value:
                raise TemplateSyntaxError('"with" in %r tag needs at least one keyword argument.' % bits[0])
        elif option == "only":
            value = True
        else:
            raise TemplateSyntaxError("Unknown argument for %r tag: %r." % (bits[0], option))

        options[option] = value

    isolated_context = options.get("only", False)
    namemap = options.get("with", {})
    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])

    return IncludeNode(
        parser.compile_filter(bits[1]),
        extra_context=namemap,
        isolated_context=isolated_context,
    )


@register.filter(takes_context=True)
def to_html(context: dict, text: str) -> str:
    """
    Converts markdown to HTML.
    """

    (html, metadata) = MarkdownRenderer.instance().render_markdown_text(text)
    rendered_html = MarkdownRenderer.instance().render_html_with_django(html, metadata, request=context["request"])

    return mark_safe(rendered_html)  # noqa: S308


@register.simple_tag
def raise_404(message: Optional[str] = None):
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
def paths(context: dict) -> List[str]:
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


class ColtraneStaticNode(StaticNode):
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


@register.tag("static")
def do_static(parser, token):
    """
    Coltrane's override for the regular Django static templatetag.

    Join the given path with the STATIC_URL setting.

    Usage::

        {% static path [as varname] %}

    Examples::

        {% static "myapp/css/base.css" %}
        {% static variable_with_path %}
        {% static "myapp/css/base.css" as admin_base_css %}
        {% static variable_with_path as varname %}
    """

    return ColtraneStaticNode.handle_token(parser, token)


class ExtendsNode(Node):
    must_be_first = True
    context_key = "extends_context"

    def __init__(self, nodelist, parent_name, template_dirs=None):
        self.nodelist = nodelist
        self.parent_name = parent_name
        self.template_dirs = template_dirs
        self.blocks = {n.name: n for n in nodelist.get_nodes_by_type(BlockNode)}

    def __repr__(self):
        return "<%s: extends %s>" % (self.__class__.__name__, self.parent_name.token)

    def find_template(self, template_name, context):
        """
        This is a wrapper around engine.find_template(). A history is kept in
        the render_context attribute between successive extends calls and
        passed as the skip argument. This enables extends to work recursively
        without extending the same template twice.
        """

        history = context.render_context.setdefault(
            self.context_key,
            [self.origin],
        )
        template, origin = context.template.engine.find_template(
            template_name,
            skip=history,
        )
        history.append(origin)

        return template

    def get_parent(self, context):
        parent = self.parent_name.resolve(context)

        if not parent:
            error_msg = "Invalid template name in 'extends' tag: %r." % parent

            if self.parent_name.filters or isinstance(self.parent_name.var, Variable):
                error_msg += " Got this from the '%s' variable." % self.parent_name.token

            raise TemplateSyntaxError(error_msg)

        if isinstance(parent, Template):
            # parent is a django.template.Template
            return parent

        if isinstance(getattr(parent, "template", None), Template):
            # parent is a django.template.backends.django.Template
            return parent.template

        # If the current request is for a custom site, target that site's template folder
        if request := context.get("request"):
            parent = get_config().get_site(request).get_template_name(parent, verify=False)

        return self.find_template(parent, context)

    def render(self, context):
        compiled_parent = self.get_parent(context)

        if BLOCK_CONTEXT_KEY not in context.render_context:
            context.render_context[BLOCK_CONTEXT_KEY] = BlockContext()

        block_context = context.render_context[BLOCK_CONTEXT_KEY]

        # Add the block nodes from this node to the block context
        block_context.add_blocks(self.blocks)

        # If this block's parent doesn't have an extends node it is the root,
        # and its block nodes also need to be added to the block context.
        for node in compiled_parent.nodelist:
            # The ExtendsNode has to be the first non-text node.
            if not isinstance(node, TextNode):
                if not isinstance(node, ExtendsNode):
                    blocks = {n.name: n for n in compiled_parent.nodelist.get_nodes_by_type(BlockNode)}
                    block_context.add_blocks(blocks)

                break

        # Call Template._render explicitly so the parser context stays
        # the same.
        with context.render_context.push_state(compiled_parent, isolated_context=False):
            return compiled_parent._render(context)


@register.tag("extends")
def do_extends(parser, token):
    """
    Signal that this template extends a parent template.

    This tag may be used in two ways: ``{% extends "base" %}`` (with quotes)
    uses the literal value "base" as the name of the parent template to extend,
    or ``{% extends variable %}`` uses the value of ``variable`` as either the
    name of the parent template to extend (if it evaluates to a string) or as
    the parent template itself (if it evaluates to a Template object).
    """

    bits = token.split_contents()

    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes one argument" % bits[0])

    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    parent_name = parser.compile_filter(bits[1])
    nodelist = parser.parse()

    if nodelist.get_nodes_by_type(ExtendsNode):
        raise TemplateSyntaxError("'%s' cannot appear more than once in the same template" % bits[0])

    return ExtendsNode(nodelist, parent_name)
