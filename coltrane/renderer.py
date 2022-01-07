import logging
from typing import Dict, Optional, Tuple

from django.conf import settings
from django.template import engines
from django.utils.html import mark_safe  # type: ignore

from markdown2 import markdown_path

from .retriever import get_data


logger = logging.getLogger(__name__)

DEFAULT_TEMPLATE = "coltrane/content.html"

DEFAULT_MARKDOWN_EXTRAS = [
    "fenced-code-blocks",
    "header-ids",
    "metadata",
    "strike",
    "tables",
    "task_list",
]


def _get_markdown_content_as_html(slug: str) -> Dict[str, Optional[Dict]]:
    """
    Converts markdown file based on the slug into HTML.
    """

    file_path = settings.BASE_DIR / "content" / f"{slug}.md"

    markdown_extras = DEFAULT_MARKDOWN_EXTRAS

    if hasattr(settings, "COLTRANE") and settings.COLTRANE.get("MARKDOWN_EXTRAS"):
        markdown_extras = settings.COLTRANE["MARKDOWN_EXTRAS"]

    content = markdown_path(
        file_path,
        extras=markdown_extras,
    )

    return (str(content), content.metadata)


def _render_html_with_django(html: str, context: Dict) -> str:
    """
    Takes the rendered HTML from the markdown uses Django to fill in any template
    variables from the `context` dictionary.
    """

    django_engine = engines["django"]
    template = django_engine.from_string(html)

    return str(template.render(context=context))


def render_markdown(slug: str) -> Tuple[str, Dict]:
    """
    Renders the markdown from the `slug` by:
    1. Rendering the markdown file into HTML
    2. Passing the HTML through Django to fill in template variables based on
        data in JSON files and markdown frontmatter

    Returns:
        Tuple of template file name (i.e. `coltrane/content.html`) and context dictionary.
    """

    (html, metadata) = _get_markdown_content_as_html(slug)

    if not metadata:
        metadata = {}

    if "template" not in metadata:
        metadata["template"] = DEFAULT_TEMPLATE

    # Start with any metadata from the markdown frontmatter
    context = metadata

    # Add JSON data to the context
    data = get_data()
    context["data"] = data

    # Add rendered content to the context
    content = _render_html_with_django(html, context)
    context["content"] = mark_safe(content)
    template = context["template"]

    return (template, context)
