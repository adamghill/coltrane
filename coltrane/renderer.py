import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

from django.http import HttpRequest
from django.template import engines
from django.utils.html import mark_safe  # type: ignore
from django.utils.timezone import now

import dateparser
from markdown2 import Markdown, markdown, markdown_path

from .config.paths import get_content_directory
from .config.settings import get_markdown_extras, get_site_url
from .retriever import get_data


logger = logging.getLogger(__name__)

DEFAULT_TEMPLATE = "coltrane/content.html"


@dataclass
class StaticRequest:
    """
    Used to mock an HttpRequest when generating the HTML for static sites.

    Required for `coltrane.templatetags.coltrane.current_direct
    """

    path: str
    META: Dict = field(default_factory=dict)
    GET: Dict = field(default_factory=dict)

    def __init__(self, path: str, meta=None, get=None):
        self.path = path
        self.META = meta or {}
        self.GET = get or {}
    
    @property
    def site_url(self):
        site_url = get_site_url()
        assert site_url, "COLTRANE_SITE_URL in .env or COLTRANE.SITE_URL in settings file is required"

        return site_url

    @property
    def scheme(self) -> str:
        return self.site_url.split("://")[0]

    def get_host(self) -> str:
        return self.site_url.split("://")[1]

    def is_secure(self) -> bool:
        return self.path.startswith("https://")


@dataclass
class RenderedMarkdown:
    content: str
    metadata: Dict


def _parse_and_update_metadata(content: Markdown) -> dict:
    """
    Add new, parse and/or cast existing values to metadata.
    """

    metadata = content.metadata

    if metadata is None:
        metadata = {}

    if "publish_date" in metadata:
        metadata["publish_date"] = dateparser.parse(metadata["publish_date"])

    if "draft" in metadata:
        metadata["draft"] = metadata["draft"] == "true"

    metadata["now"] = now()

    if hasattr(content, "toc_html"):
        metadata["toc"] = mark_safe(content.toc_html)

    return metadata


def _get_markdown_content_as_html(slug: str) -> RenderedMarkdown:
    """
    Converts markdown file based on the slug into HTML.
    """

    path = get_content_directory() / f"{slug}.md"

    return render_markdown_path(path)


def render_markdown_path(path: Path) -> RenderedMarkdown:
    """
    Renders the markdown file located at path.
    """

    markdown_extras = get_markdown_extras()
    content = markdown_path(
        path,
        extras=markdown_extras,
    )
    metadata = _parse_and_update_metadata(content)

    return RenderedMarkdown(str(content), metadata)


def render_markdown_text(text: str) -> RenderedMarkdown:
    """
    Renders the markdown text.
    """

    markdown_extras = get_markdown_extras()
    content = markdown(text, extras=markdown_extras)
    metadata = _parse_and_update_metadata(content)

    return RenderedMarkdown(str(content), metadata)


def render_html_with_django(
    rendered_markdown: RenderedMarkdown, request: HttpRequest = None
) -> str:
    """
    Takes the rendered HTML from the markdown uses Django to fill in any template
    variables from the `context` dictionary.
    """

    django_engine = engines["django"]
    template = django_engine.from_string(rendered_markdown.content)

    return str(template.render(context=rendered_markdown.metadata, request=request))


def get_html_and_markdown(slug: str) -> RenderedMarkdown:
    rendered_markdown = _get_markdown_content_as_html(slug)
    metadata = rendered_markdown.metadata

    if metadata is None:
        metadata = {}

    if "template" not in metadata:
        metadata["template"] = DEFAULT_TEMPLATE

    metadata["slug"] = slug

    rendered_markdown.metadata = metadata

    return rendered_markdown


def render_markdown(
    slug: str, request: Union[HttpRequest, StaticRequest]
) -> RenderedMarkdown:
    """
    Renders the markdown from the `slug` by:
    1. Rendering the markdown file into HTML
    2. Passing the HTML through Django to fill in template variables based on
        data in JSON files and markdown frontmatter

    Returns:
        `RenderedMarkdown` with template file name (i.e. `coltrane/content.html`) and context dictionary.
    """

    rendered_markdown = get_html_and_markdown(slug)

    context = {}

    # Start with any metadata from the markdown frontmatter
    context.update(rendered_markdown.metadata)

    # Add JSON data to the context
    data = get_data()
    context["data"] = data

    if request:
        context["request"] = request

    # Add rendered content to the context
    content = render_html_with_django(rendered_markdown, request)
    context["content"] = mark_safe(content)
    template = context["template"]

    return RenderedMarkdown(template, context)
