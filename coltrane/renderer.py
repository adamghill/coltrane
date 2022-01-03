import logging
from typing import Dict, Tuple

from django.conf import settings
from django.template import engines

from markdown2 import markdown_path

from .retriever import get_data


logger = logging.getLogger(__name__)


def _get_markdown_content_as_html(slug: str) -> str:
    """
    Converts markdown file based on the slug into HTML.
    """

    markdown_file_path = settings.BASE_DIR / "content" / f"{slug}.md"

    content = markdown_path(
        markdown_file_path,
        extras=[
            "fenced-code-blocks",
            "header-ids",
            "metadata",
            "strike",
            "tables",
            "task_list",
            "nofollow",
            # "code-friendly",
        ],
    )

    return str(content)


def _get_rendered_content(markdown_content: str, data: Dict) -> str:
    django_engine = engines["django"]
    template = django_engine.from_string(markdown_content)

    return str(template.render(context={"data": data}))


def render_markdown(slug: str) -> Tuple[str, Dict]:
    markdown_content = _get_markdown_content_as_html(slug)
    data = get_data()
    rendered_content = _get_rendered_content(markdown_content, data)

    return (rendered_content, data)
