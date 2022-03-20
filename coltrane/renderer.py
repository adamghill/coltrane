import logging
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, Union

from django.conf import settings
from django.http import HttpRequest
from django.template import engines
from django.utils.html import mark_safe  # type: ignore
from django.utils.timezone import now

import dateparser
from markdown2 import markdown_path

from .config.paths import get_content_directory
from .config.settings import get_markdown_extras
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

    @property
    def site(self):
        _site = settings.COLTRANE.get("SITE")
        assert _site, "COLTRANE_SITE is required in .env"

        return _site

    @property
    def scheme(self) -> str:
        return self.site.split("://")[0]

    def get_host(self) -> str:
        return self.site.split("://")[1]

    def is_secure(self) -> bool:
        return self.path.startswith("https://")


def render_markdown_path(path) -> Dict[str, Optional[Dict]]:
    """
    Renders the markdown file located at path.
    """

    markdown_extras = get_markdown_extras()

    content = markdown_path(
        path,
        extras=markdown_extras,
    )

    metadata = content.metadata

    if metadata is None:
        metadata = {}

    if "date" in metadata:
        metadata["date"] = dateparser.parse(metadata["date"])

    if "draft" in metadata:
        metadata["draft"] = metadata["draft"] == "true"

    metadata["now"] = now()

    if hasattr(content, "toc_html"):
        metadata["toc"] = mark_safe(content.toc_html)

    return (str(content), metadata)


def _get_markdown_content_as_html(slug: str) -> Dict[str, Optional[Dict]]:
    """
    Converts markdown file based on the slug into HTML.
    """

    path = get_content_directory() / f"{slug}.md"

    return render_markdown_path(path)


def render_html_with_django(
    html: str, context: Dict, request: HttpRequest = None
) -> str:
    """
    Takes the rendered HTML from the markdown uses Django to fill in any template
    variables from the `context` dictionary.
    """

    django_engine = engines["django"]
    template = django_engine.from_string(html)

    return str(template.render(context=context, request=request))


def get_html_and_markdown(slug: str) -> Tuple[str, Dict]:
    (html, metadata) = _get_markdown_content_as_html(slug)

    if metadata is None:
        metadata = {}

    if "template" not in metadata:
        metadata["template"] = DEFAULT_TEMPLATE

    metadata["slug"] = slug

    return (html, metadata)


def render_markdown(
    slug: str, request: Union[HttpRequest, StaticRequest]
) -> Tuple[str, Dict]:
    """
    Renders the markdown from the `slug` by:
    1. Rendering the markdown file into HTML
    2. Passing the HTML through Django to fill in template variables based on
        data in JSON files and markdown frontmatter

    Returns:
        Tuple of template file name (i.e. `coltrane/content.html`) and context dictionary.
    """

    (html, metadata) = get_html_and_markdown(slug)

    context = {}

    # Start with any metadata from the markdown frontmatter
    context.update(metadata)

    # Add JSON data to the context
    data = get_data()
    context["data"] = data

    if request:
        context["request"] = request

    # Add rendered content to the context
    content = render_html_with_django(html, context, request)
    context["content"] = mark_safe(content)
    template = context["template"]

    return (template, context)
