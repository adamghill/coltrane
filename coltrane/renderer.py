import codecs
import logging
import re
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, Union

from django.http import HttpRequest
from django.template import engines
from django.utils.html import mark_safe  # type: ignore
from django.utils.timezone import now

import dateparser
from markdown2 import Markdown, markdown

from .config.paths import get_content_directory
from .config.settings import get_markdown_extras, get_site_url
from .retriever import get_data


logger = logging.getLogger(__name__)

DEFAULT_TEMPLATE = "coltrane/content.html"


@dataclass
class StaticRequest(HttpRequest):
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
        return str(self.site_url.split("://")[0])

    def get_host(self) -> str:
        return str(self.site_url.split("://")[1])

    def is_secure(self) -> bool:
        return self.path.startswith("https://")


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


def render_markdown_path(path) -> Tuple[str, Dict]:
    """
    Renders the markdown file located at path.
    """

    with codecs.open(path, "r", encoding="utf-8") as f:
        text = f.read()

        return render_markdown_text(text)


def render_markdown_text(text: str) -> Tuple[str, Dict]:
    markdown_extras = get_markdown_extras()

    # Wrap code fences with Django `verbatim` templatetag
    text = re.sub(pattern=r"```.*?```", repl="{% verbatim %}\n\g<0>\n{% endverbatim %}", string=text, flags=re.RegexFlag.DOTALL)

    content = markdown(
        text=text,
        extras=markdown_extras
    )

    metadata = _parse_and_update_metadata(content)

    # Remove `p` tags that get added to the `verbatim` templatetag
    content = content.replace("<p>{% verbatim %}</p>\n", "{% verbatim %}")
    content = content.replace("\n<p>{% endverbatim %}</p>", "{% endverbatim %}")

    return (str(content), metadata)


def _get_markdown_content_as_html(slug: str) -> Tuple[str, Optional[Dict]]:
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
